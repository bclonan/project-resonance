#pragma once

#include <vector>
#include <map>
#include <cstdint>
#include <string>
#include <deque>
#include <array>

// Forward declaration for pybind11
namespace pybind11
{
    class module_;
}

namespace phicomp
{
    namespace core
    {

        using Symbol = uint8_t;
        using ContextKey = std::string;
        using SymbolCounts = std::map<Symbol, uint32_t>;
        using ContextTree = std::map<ContextKey, SymbolCounts>;

        class FibonacciContextModel
        {
        public:
            explicit FibonacciContextModel(const std::vector<size_t> &orders = {2, 3, 5, 8, 13});
            void update(Symbol symbol) noexcept;
            std::vector<double> get_probabilities() const;

        private:
            std::vector<size_t> fib_orders;
            size_t max_order;
            std::vector<ContextTree> context_models;
            std::deque<Symbol> history;
            const double phi;
        };

        class ArithmeticCoder
        {
        public:
            std::vector<Symbol> encode(const std::vector<Symbol> &data);
            std::vector<Symbol> decode(const std::vector<Symbol> &compressed_data, size_t original_size);

        private:
            uint64_t low, high, pending_bits, code_value;
            std::vector<Symbol> bit_buffer;
            const std::vector<Symbol> *input_buffer_ptr;
            size_t bit_idx;
            void write_bit(uint8_t bit);
            void flush_encoder();
            uint8_t read_bit();
        };

        // ----------------------------------------------------------------------------
        // Lightweight global options & RGBD state (experimental bias integration)
        // ----------------------------------------------------------------------------
        struct GlobalOptions
        {
            bool use_rgbd = false;
            double rgbd_phi_weight = 0.15; // blending strength for RGBD cell bias
            static GlobalOptions &instance()
            {
                static GlobalOptions inst;
                return inst;
            }
        };

        struct RGBDState
        {
            // Tensor slices represented as last symbol + visit count per (t,x,y)
            // t dimension length 60, x,y 10 each.
            uint16_t visits[60][10][10] = {0};
            uint8_t last_symbol[60][10][10] = {0};
            // Fibonacci rolling values (mod 10) to avoid big integers.
            uint32_t fib_n = 0;   // F(n) mod 10
            uint32_t fib_np1 = 1; // F(n+1) mod 10
            uint64_t index = 0;   // number of symbols processed so far

            inline void advance_fib()
            {
                // Advance sequence while keeping mod 10 for addressing.
                uint32_t next = (fib_n + fib_np1) % 10; // F(n+2) mod 10
                fib_n = fib_np1;
                fib_np1 = next;
            }

            inline void update(uint8_t symbol)
            {
                // Compute current coordinates BEFORE incrementing index for next position bias.
                uint32_t x = fib_n % 10;   // F(n) % 10
                uint32_t y = fib_np1 % 10; // F(n+1) % 10
                uint32_t t = index % 60;   // temporal slice
                last_symbol[t][x][y] = symbol;
                if (visits[t][x][y] < 0xFFFF)
                    visits[t][x][y]++;
                // Prepare for next position
                advance_fib();
                index++;
            }

            inline void apply_bias(std::vector<double> &probabilities) const
            {
                if (!GlobalOptions::instance().use_rgbd || index == 0)
                    return;              // nothing to do yet
                uint32_t x = fib_n % 10; // position for NEXT symbol prediction
                uint32_t y = fib_np1 % 10;
                uint32_t t = index % 60;
                uint16_t v = visits[t][x][y];
                if (v == 0)
                    return;
                uint8_t sym = last_symbol[t][x][y];
                double w = GlobalOptions::instance().rgbd_phi_weight * (double)v / (double)(v + 10.0);
                probabilities[sym] += w; // add bonus
                // Renormalize to keep a valid distribution
                double sum = 0.0;
                for (double p : probabilities)
                    sum += p;
                if (sum > 0.0)
                {
                    for (double &p : probabilities)
                        p /= sum;
                }
            }
        };

        // Internal C++ functions
        std::vector<Symbol> compress_internal(const std::vector<Symbol> &data);
        std::vector<Symbol> decompress_internal(const std::vector<Symbol> &data, uint64_t original_size);

    } // namespace core
} // namespace phicomp