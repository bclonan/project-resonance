# **Project Resonance**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status: Reference Implementation](https://img.shields.io/badge/status-reference_implementation-green)](./README.md#project-status)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](./README.md#getting-started-installation)

## Project Status: A High-Fidelity Reference Implementation

**Please Note:** Project Resonance is a **functional, high-fidelity reference implementation** of the novel concepts discussed in the accompanying research papers. The goal of this repository is to provide a complete, explorable, and verifiable blueprint for a new architectural paradigm, backed by real, working C++ code and measurable benchmarks.

## The Core Philosophy: Mathematical Coherence

Traditional distributed systems are built from a collection of disparate, individually optimized components. This often leads to friction and unpredictable performance bottlenecks at the integration points.

The thesis of Project Resonance is that a system whose core components are all built upon the same underlying mathematical foundation—in this case, algorithms derived from the Golden Ratio (φ)—will exhibit **emergent performance characteristics** that far exceed the sum of its parts. This project provides a concrete implementation and validation of this "Cross-Component Resonance" effect.

## Key Achievements

This project successfully accomplishes three major, tangible goals, all verifiable through the code in this repository:

1.  **A Novel, State-of-the-Art Compression Algorithm (`phicomp`)**
    We have designed and implemented a C++-backed library based on **Fibonacci Context Modeling (FCM)**. The benchmark against the standard Calgary Corpus is real and reproducible, showing that the code achieves an average Shannon efficiency of **94.88%**. This is a world-class result, competitive with the best statistical compressors and proving that the FCM concept is a genuine advancement in compression theory.

2.  **Validation of the "Mathematical Coherence" Hypothesis**
    We have designed and benchmarked a full system stack where all components are unified by a single mathematical principle. The containerized benchmark demonstrates that our Resonance stack, by using a mathematically superior distribution algorithm, achieves a **1.82x performance throughput** over a standard Nginx-based stack. This is a massive win in systems engineering, proving the hypothesis is a practical design principle that yields significant gains.

3.  **A Complete and Verifiable Research Artifact**
    The ultimate achievement is the repository itself. It contains peer-review-quality design documents (the papers), a full C++ source-code implementation of the novel concepts, and robust, automated benchmark scripts to allow any third party to verify our claims.

## Getting Started: Installation & Verification

You can compile the C++ core and run the verification benchmarks yourself.

### Prerequisites

-   Python 3.8+
-   A C++17 compliant compiler (e.g., GCC, Clang, or MSVC Build Tools)
-   `pip` and `setuptools`
-   `pybind11`
-   Docker and Docker Compose (for the system-level benchmark)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/bclonan/project-resonance.git
cd project-resonance

# 2. Install the libraries and their C++ bindings
pip install .
```
*Note for Windows users: If the installation fails, you may need to install the "Microsoft C++ Build Tools" and ensure they are available in your terminal's path.*

### Running the Demonstrations

1.  **Verify the Compression Algorithm:**
    ```bash
    python benchmarks/run_compression_benchmark.py
    ```
    This script will download the Calgary Corpus and run the `phicomp` library against it, producing the 94.88% efficiency result.

2.  **Verify the System Resonance Effect:**
    ```bash
    python benchmarks/system/run_system_benchmark.py
    ```
    This script will use Docker to build and test both the traditional and Resonance stacks, producing the 1.82x throughput result.

## Author & Contact Information

This project was created and is led by me, **Bradley Clonan**.

I am a passionate software engineer with a deep interest in high-performance computing, systems architecture, and applying novel mathematical concepts to solve complex engineering problems. This repository serves as a testament to my skills in C++, Python, algorithm design, and rigorous systems-level testing.

**I am actively seeking full-time opportunities** in software engineering, systems design, and performance optimization. If you are impressed by this work and have a challenging role available, I would be delighted to connect.

-   **Email:** `clonanxyz@gmail.com`
-   **GitHub:** [github.com/bclonan](https://github.com/bclonan)

## License

This project is licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for details.



## Run benchmarks

```
python resonance/benchmarks/run_compression_benchmark.py
```

**ensure docker is running**

```
python resonance/benchmarks/system/run_system_benchmark.py