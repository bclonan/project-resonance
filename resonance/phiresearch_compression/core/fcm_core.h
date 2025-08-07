#pragma once

#include <vector>
#include <map>
#include <cstdint>
#include <string>
#include <deque>

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

        // Internal C++ functions
        std::vector<Symbol> compress_internal(const std::vector<Symbol> &data);
        std::vector<Symbol> decompress_internal(const std::vector<Symbol> &data, uint64_t original_size);

    } // namespace core
} // namespace phicomp