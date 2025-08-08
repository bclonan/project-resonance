#include "fcm_core.h"
#include <cmath>
#include <numeric>
#include <algorithm>
#include <stdexcept>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace phicomp
{
    namespace core
    {

        const double GOLDEN_RATIO = (1.0 + std::sqrt(5.0)) / 2.0;

        // --- FibonacciContextModel Implementation ---
        FibonacciContextModel::FibonacciContextModel(const std::vector<size_t> &orders)
            : phi(GOLDEN_RATIO), fib_orders(orders)
        {
            if (orders.empty())
                throw std::invalid_argument("Fibonacci orders cannot be empty.");
            context_models.resize(fib_orders.size());
            max_order = fib_orders.back();
        }

        void FibonacciContextModel::update(Symbol symbol) noexcept
        {
            for (size_t i = 0; i < fib_orders.size(); ++i)
            {
                size_t order = fib_orders[i];
                if (history.size() >= order)
                {
                    ContextKey context(history.begin() + (history.size() - order), history.end());
                    context_models[i][context][symbol]++;
                }
            }
            history.push_back(symbol);
            if (history.size() > max_order)
                history.pop_front();
        }

        std::vector<double> FibonacciContextModel::get_probabilities() const
        {
            std::vector<double> final_probabilities(256, 0.0);
            double total_weight = 0.0;
            for (int i = fib_orders.size() - 1; i >= 0; --i)
            {
                size_t order = fib_orders[i];
                if (history.size() < order)
                    continue;
                ContextKey context(history.begin() + (history.size() - order), history.end());
                auto model_it = context_models[i].find(context);
                if (model_it != context_models[i].end())
                {
                    double weight = std::pow(phi, (double)i);
                    const SymbolCounts &counts = model_it->second;
                    uint32_t context_total = 0;
                    for (const auto &pair : counts)
                        context_total += pair.second;
                    if (context_total > 0)
                    {
                        for (const auto &pair : counts)
                        {
                            final_probabilities[pair.first] += weight * ((double)pair.second / context_total);
                        }
                        total_weight += weight;
                    }
                }
            }
            double escape_prob = std::pow(phi, -(double)fib_orders.size());
            if (total_weight > 0.0)
            {
                for (size_t k = 0; k < 256; ++k)
                {
                    final_probabilities[k] = (final_probabilities[k] / total_weight) * (1.0 - escape_prob);
                }
            }
            else
            {
                escape_prob = 1.0;
            }
            for (size_t k = 0; k < 256; ++k)
            {
                final_probabilities[k] += escape_prob / 256.0;
            }
            return final_probabilities;
        }

        // --- ArithmeticCoder Implementation ---
        void ArithmeticCoder::write_bit(uint8_t bit) { bit_buffer.push_back(bit); }

        void ArithmeticCoder::flush_encoder()
        {
            pending_bits++;
            write_bit((low < (1ULL << 62)) ? 0 : 1);
            for (uint64_t i = 0; i < pending_bits - 1; ++i)
            {
                write_bit(~((low < (1ULL << 62)) ? 0 : 1) & 1);
            }
        }

        uint8_t ArithmeticCoder::read_bit()
        {
            if (bit_idx >= input_buffer_ptr->size() * 8)
                return 0;
            size_t byte_pos = bit_idx / 8;
            size_t bit_pos_in_byte = 7 - (bit_idx % 8);
            bit_idx++;
            return ((*input_buffer_ptr)[byte_pos] >> bit_pos_in_byte) & 1;
        }

        static RGBDState g_rgbd_state; // single process-local state (stateless compression would isolate)

        std::vector<Symbol> ArithmeticCoder::encode(const std::vector<Symbol> &data)
        {
            // Ensure RGBD state starts clean for each independent encoding so that
            // decode reproduces identical probability sequence.
            g_rgbd_state = RGBDState();
            static const uint64_t TOP_VALUE = ~0ULL;
            static const uint64_t HALF = 1ULL << 63;
            static const uint64_t FIRST_QUARTER = 1ULL << 62;
            static const uint64_t THIRD_QUARTER = 3ULL << 62;
            low = 0;
            high = TOP_VALUE;
            pending_bits = 0;
            bit_buffer.clear();
            FibonacciContextModel model;
            for (Symbol symbol : data)
            {
                // Build integer cumulative frequencies for stable mapping
                std::vector<double> probabilities = model.get_probabilities();
                g_rgbd_state.apply_bias(probabilities);
                // Floor tiny/negative and renormalize
                double sum_prob = 0.0;
                for (double &p : probabilities)
                {
                    if (p <= 0.0)
                        p = 1e-12;
                    sum_prob += p;
                }
                if (sum_prob <= 0.0)
                {
                    for (double &p : probabilities)
                        p = 1.0 / 256.0;
                }
                else
                {
                    for (double &p : probabilities)
                        p /= sum_prob;
                }
                const uint32_t TOTAL_FREQ = 1u << 16; // 65536
                std::array<uint32_t, 256> freq{};
                std::array<double, 256> frac{};
                uint64_t sum_f = 0;
                for (size_t i = 0; i < 256; ++i)
                {
                    double raw = probabilities[i] * (double)TOTAL_FREQ;
                    uint32_t base = (uint32_t)std::floor(raw);
                    if (base < 1)
                        base = 1;
                    freq[i] = base;
                    frac[i] = raw - std::floor(raw);
                    sum_f += base;
                }
                // Adjust to match TOTAL_FREQ
                if (sum_f < TOTAL_FREQ)
                {
                    uint32_t rem = TOTAL_FREQ - (uint32_t)sum_f;
                    // Distribute to largest fractional parts
                    std::array<size_t, 256> idx{};
                    for (size_t i = 0; i < 256; ++i)
                        idx[i] = i;
                    std::stable_sort(idx.begin(), idx.end(), [&](size_t a, size_t b)
                                     { return frac[a] > frac[b]; });
                    for (uint32_t k = 0; k < rem; ++k)
                        freq[idx[k % 256]]++;
                }
                else if (sum_f > TOTAL_FREQ)
                {
                    uint32_t over = (uint32_t)sum_f - TOTAL_FREQ;
                    // Remove from smallest fractional parts but keep >=1
                    std::array<size_t, 256> idx{};
                    for (size_t i = 0; i < 256; ++i)
                        idx[i] = i;
                    std::stable_sort(idx.begin(), idx.end(), [&](size_t a, size_t b)
                                     { return frac[a] < frac[b]; });
                    size_t k = 0;
                    while (over > 0)
                    {
                        size_t id = idx[k % 256];
                        if (freq[id] > 1)
                        {
                            freq[id]--;
                            --over;
                        }
                        ++k;
                    }
                }
                std::array<uint32_t, 257> cum{};
                cum[0] = 0;
                for (size_t i = 0; i < 256; ++i)
                    cum[i + 1] = cum[i] + freq[i];
                // Map symbol into range using integer cumulative frequencies
                uint64_t range = high - low + 1;
                uint64_t low_off = (uint64_t)((long double)range * (long double)cum[symbol] / (long double)TOTAL_FREQ);
                uint64_t high_off = (uint64_t)((long double)range * (long double)cum[symbol + 1] / (long double)TOTAL_FREQ);
                low = low + low_off;
                high = low + high_off - low_off - 1;
                while (true)
                {
                    if (high < HALF)
                    {
                        write_bit(0);
                        while (pending_bits > 0)
                        {
                            write_bit(1);
                            pending_bits--;
                        }
                    }
                    else if (low >= HALF)
                    {
                        write_bit(1);
                        while (pending_bits > 0)
                        {
                            write_bit(0);
                            pending_bits--;
                        }
                        low -= HALF;
                        high -= HALF;
                    }
                    else if (low >= FIRST_QUARTER && high < THIRD_QUARTER)
                    {
                        pending_bits++;
                        low -= FIRST_QUARTER;
                        high -= FIRST_QUARTER;
                    }
                    else
                    {
                        break;
                    }
                    low <<= 1;
                    high <<= 1;
                    high |= 1;
                }
                model.update(symbol);
                // Update RGBD state after processing symbol so next prediction uses new context.
                g_rgbd_state.update(symbol);
            }
            flush_encoder();
            std::vector<Symbol> byte_output;
            byte_output.reserve(bit_buffer.size() / 8 + 1);
            for (size_t i = 0; i < bit_buffer.size(); i += 8)
            {
                Symbol byte = 0;
                for (size_t j = 0; j < 8; ++j)
                {
                    byte <<= 1;
                    if (i + j < bit_buffer.size())
                        byte |= bit_buffer[i + j];
                }
                byte_output.push_back(byte);
            }
            return byte_output;
        }

        std::vector<Symbol> ArithmeticCoder::decode(const std::vector<Symbol> &compressed_data, size_t original_size)
        {
            if (original_size == 0)
                return {};
            // Reset RGBD state so probability evolution mirrors encoding run.
            g_rgbd_state = RGBDState();
            static const uint64_t TOP_VALUE = ~0ULL;
            static const uint64_t HALF = 1ULL << 63;
            static const uint64_t FIRST_QUARTER = 1ULL << 62;
            static const uint64_t THIRD_QUARTER = 3ULL << 62;
            input_buffer_ptr = &compressed_data;
            bit_idx = 0;
            code_value = 0;
            for (size_t i = 0; i < 64; ++i)
                code_value = (code_value << 1) | read_bit();
            low = 0;
            high = TOP_VALUE;
            FibonacciContextModel model;
            std::vector<Symbol> output_data;
            output_data.reserve(original_size);
            for (size_t i = 0; i < original_size; ++i)
            {
                // Build integer cumulative frequencies matching encoder
                std::vector<double> probabilities = model.get_probabilities();
                g_rgbd_state.apply_bias(probabilities);
                double sum_prob_d = 0.0;
                for (double &p : probabilities)
                {
                    if (p <= 0.0)
                        p = 1e-12;
                    sum_prob_d += p;
                }
                if (sum_prob_d <= 0.0)
                {
                    for (double &p : probabilities)
                        p = 1.0 / 256.0;
                }
                else
                {
                    for (double &p : probabilities)
                        p /= sum_prob_d;
                }
                const uint32_t TOTAL_FREQ = 1u << 16;
                std::array<uint32_t, 256> freq{};
                std::array<double, 256> frac{};
                uint64_t sum_f = 0;
                for (size_t j = 0; j < 256; ++j)
                {
                    double raw = probabilities[j] * (double)TOTAL_FREQ;
                    uint32_t base = (uint32_t)std::floor(raw);
                    if (base < 1)
                        base = 1;
                    freq[j] = base;
                    frac[j] = raw - std::floor(raw);
                    sum_f += base;
                }
                if (sum_f < TOTAL_FREQ)
                {
                    uint32_t rem = TOTAL_FREQ - (uint32_t)sum_f;
                    std::array<size_t, 256> idx{};
                    for (size_t j = 0; j < 256; ++j)
                        idx[j] = j;
                    std::stable_sort(idx.begin(), idx.end(), [&](size_t a, size_t b)
                                     { return frac[a] > frac[b]; });
                    for (uint32_t k = 0; k < rem; ++k)
                        freq[idx[k % 256]]++;
                }
                else if (sum_f > TOTAL_FREQ)
                {
                    uint32_t over = (uint32_t)sum_f - TOTAL_FREQ;
                    std::array<size_t, 256> idx{};
                    for (size_t j = 0; j < 256; ++j)
                        idx[j] = j;
                    std::stable_sort(idx.begin(), idx.end(), [&](size_t a, size_t b)
                                     { return frac[a] < frac[b]; });
                    size_t k = 0;
                    while (over > 0)
                    {
                        size_t id = idx[k % 256];
                        if (freq[id] > 1)
                        {
                            freq[id]--;
                            --over;
                        }
                        ++k;
                    }
                }
                std::array<uint32_t, 257> cum{};
                cum[0] = 0;
                for (size_t j = 0; j < 256; ++j)
                    cum[j + 1] = cum[j] + freq[j];
                // Determine symbol using integer scaled value
                uint64_t range = high - low + 1;
                long double sv = ((((long double)code_value - (long double)low) + 1.0L) * (long double)TOTAL_FREQ - 1.0L) / (long double)range;
                uint32_t scaled = (uint32_t)std::floor(std::max<long double>(0.0L, sv));
                if (scaled >= TOTAL_FREQ)
                    scaled = TOTAL_FREQ - 1;
                Symbol decoded_symbol = 255;
                for (size_t s = 0; s < 256; ++s)
                {
                    if (scaled < cum[s + 1])
                    {
                        decoded_symbol = static_cast<Symbol>(s);
                        break;
                    }
                }
                output_data.push_back(decoded_symbol);
                // Update range with integer cumulative frequencies
                uint64_t low_off = (uint64_t)((long double)range * (long double)cum[decoded_symbol] / (long double)TOTAL_FREQ);
                uint64_t high_off = (uint64_t)((long double)range * (long double)cum[decoded_symbol + 1] / (long double)TOTAL_FREQ);
                low = low + low_off;
                high = low + high_off - low_off - 1;
                while (true)
                {
                    if (high < HALF)
                    {
                    }
                    else if (low >= HALF)
                    {
                        low -= HALF;
                        high -= HALF;
                        code_value -= HALF;
                    }
                    else if (low >= FIRST_QUARTER && high < THIRD_QUARTER)
                    {
                        low -= FIRST_QUARTER;
                        high -= FIRST_QUARTER;
                        code_value -= FIRST_QUARTER;
                    }
                    else
                    {
                        break;
                    }
                    low <<= 1;
                    high <<= 1;
                    high |= 1;
                    code_value <<= 1;
                    code_value |= read_bit();
                }
                model.update(decoded_symbol);
                g_rgbd_state.update(decoded_symbol);
            }
            return output_data;
        }

        // --- Internal C++ API Functions ---
        std::vector<Symbol> compress_internal(const std::vector<Symbol> &data)
        {
            ArithmeticCoder coder;
            return coder.encode(data);
        }

        std::vector<Symbol> decompress_internal(const std::vector<Symbol> &data, uint64_t original_size)
        {
            ArithmeticCoder coder;
            auto decompressed_data = coder.decode(data, original_size);
            if (decompressed_data.size() != original_size)
            {
                throw std::runtime_error("Decompression failed: size mismatch.");
            }
            return decompressed_data;
        }

    } // namespace core
} // namespace phicomp

// =================================================================================
//  pybind11 Module Definition
// =================================================================================
PYBIND11_MODULE(core_bindings, m)
{
    m.doc() = "Production-grade C++ core for PhiComp compression";

    m.def("set_rgbd_options", [](bool use_rgbd, double weight)
          {
              phicomp::core::GlobalOptions::instance().use_rgbd = use_rgbd;
              if (weight > 0.0) phicomp::core::GlobalOptions::instance().rgbd_phi_weight = weight; }, pybind11::arg("use_rgbd"), pybind11::arg("weight") = 0.0, "Configure experimental RGBD bias integration (use cautiously; non-deterministic if state reused).");

    m.def("reset_rgbd_state", []()
          { phicomp::core::g_rgbd_state = phicomp::core::RGBDState(); }, "Reset internal RGBD lattice state (call before independent compression tasks).");

    m.def("compress_main", [](const pybind11::bytes &data_bytes)
          {
        std::string data_str = data_bytes;
        std::vector<phicomp::core::Symbol> data_vec(data_str.begin(), data_str.end());
        
        auto compressed_body = phicomp::core::compress_internal(data_vec);
        
        std::string header = "PHIC\x01\x01";
        header.resize(14);
        uint64_t original_size = data_vec.size();
        for (int i = 0; i < 8; ++i) {
            header[6 + i] = (original_size >> (i * 8)) & 0xFF;
        }
        header.append(reinterpret_cast<const char*>(compressed_body.data()), compressed_body.size());
        
        return pybind11::bytes(header); }, "Compresses data using adaptive FCM and Arithmetic Coding");

    m.def("decompress_main", [](const pybind11::bytes &data_bytes)
          {
        std::string data_str = data_bytes;
        if (data_str.size() < 14) throw std::runtime_error("Invalid PhiComp data: header too short.");
        if (data_str.substr(0, 4) != "PHIC") throw std::runtime_error("Invalid PhiComp data: magic number mismatch.");
        
        uint64_t original_size = 0;
        for (int i = 0; i < 8; ++i) {
            original_size |= static_cast<uint64_t>(static_cast<phicomp::core::Symbol>(data_str[6 + i])) << (i * 8);
        }
        
        std::vector<phicomp::core::Symbol> compressed_body(data_str.begin() + 14, data_str.end());
        auto decompressed_vec = phicomp::core::decompress_internal(compressed_body, original_size);
        
        std::string decompressed_str(decompressed_vec.begin(), decompressed_vec.end());
    return pybind11::bytes(decompressed_str); }, "Decompresses data compressed with PhiComp");
}