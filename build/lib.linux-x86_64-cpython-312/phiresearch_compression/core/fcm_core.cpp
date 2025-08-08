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

        std::vector<Symbol> ArithmeticCoder::encode(const std::vector<Symbol> &data)
        {
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
                uint64_t range = high - low + 1;
                std::vector<double> probabilities = model.get_probabilities();
                double cum_prob_low = 0.0;
                for (int i = 0; i < symbol; ++i)
                    cum_prob_low += probabilities[i];
                high = low + static_cast<uint64_t>(range * (cum_prob_low + probabilities[symbol])) - 1;
                low = low + static_cast<uint64_t>(range * cum_prob_low);
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
                uint64_t range = high - low + 1;
                std::vector<double> probabilities = model.get_probabilities();
                uint64_t total_freq = 1ULL << 32;
                uint64_t scaled_value = ((code_value - low + 1) * total_freq - 1) / range;
                double cum_prob = 0.0;
                Symbol decoded_symbol = 255;
                for (size_t s = 0; s < 256; ++s)
                {
                    cum_prob += probabilities[s];
                    if (scaled_value < static_cast<uint64_t>(cum_prob * total_freq))
                    {
                        decoded_symbol = static_cast<Symbol>(s);
                        break;
                    }
                }
                output_data.push_back(decoded_symbol);
                double cum_prob_low = 0.0;
                for (int k = 0; k < decoded_symbol; ++k)
                    cum_prob_low += probabilities[k];
                high = low + static_cast<uint64_t>(range * (cum_prob_low + probabilities[decoded_symbol])) - 1;
                low = low + static_cast<uint64_t>(range * cum_prob_low);
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