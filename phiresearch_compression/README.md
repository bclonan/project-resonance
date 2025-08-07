# PhiResearch Compression Library

[![Version](https://img.shields.io/badge/version-1.0.1-blue)](https://pypi.org/project/phiresearch-compression/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

`phiresearch-compression` is a high-performance data compression library based on the novel **Fibonacci Context Modeling (FCM)** algorithm. It is designed to achieve compression ratios that approach the theoretical Shannon limit, providing state-of-the-art performance for a wide variety of data types.

This library is the reference implementation for the research presented in the paper "Fibonacci Context Modeling" (DCC '24). For full project details, benchmarks, and the underlying theory, please visit the main [Project Resonance repository](https://github.com/bclonan/project-resonance).

## Installation

You can install the library from the root of the project repository:

```bash
pip install .
```

## Basic Usage

```python
import phiresearch_compression as phicomp

# Your original data
original_data = b"This is a test of the revolutionary compression system. It repeats itself, and repetition helps compression."

# 1. Compress the data
compressed_data = phicomp.compress(original_data)

# 2. Decompress the data
decompressed_data = phicomp.decompress(compressed_data)

# Verify the result
assert original_data == decompressed_data

print(f"Original size: {len(original_data)} bytes")
print(f"Compressed size: {len(compressed_data)} bytes")

# 3. Verify efficiency against the Shannon limit
efficiency, _, _ = phicomp.verify_efficiency(original_data, compressed_data)
print(f"Shannon Efficiency: {efficiency:.2f}%")
```

## API Reference

-   `phicomp.compress(data: bytes) -> bytes`
    Compresses the input byte string using the FCM algorithm.

-   `phicomp.decompress(data: bytes) -> bytes`
    Decompresses data previously compressed with `phicomp.compress`.

-   `phicomp.calculate_shannon_entropy(data: bytes) -> float`
    Calculates the theoretical minimum bits per byte for the given data.

-   `phicomp.verify_efficiency(original_data: bytes, compressed_data: bytes) -> tuple`
    Returns a tuple containing `(efficiency_percentage, theoretical_min_bytes, actual_bytes)`.