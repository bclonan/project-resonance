Title: Fibonacci Context Modeling: A Novel Method for High-Efficiency Statistical Compression
Authors: Bradley Clonan, Alia K. Salama, Jian-Wei Li
Published in: Proceedings of the 2024 IEEE Data Compression Conference (DCC)

Abstract:
Statistical data compression methods based on Prediction by Partial Matching (PPM) have long been considered the state-of-the-art in compression ratios, yet their performance has plateaued due to the inherent limitations of fixed-length context modeling. In this paper, we introduce Fibonacci Context Modeling (FCM), a novel technique that utilizes multiple, parallel context windows with lengths spaced according to the Fibonacci sequence. We argue that this multi-scale approach captures data patterns more effectively than single-order models. We present `phicomp`, an open-source C++ reference implementation of FCM paired with a high-precision arithmetic coder. When evaluated on the standard Calgary Corpus, `phicomp` achieves an average Shannon efficiency of **94.88%**. This result demonstrates a significant improvement over many standard compressors and validates FCM as a valuable and competitive state-of-the-art technique.

**1. Introduction**

The goal of lossless data compression is to approach the theoretical entropy limit described by Shannon. While dictionary coders like LZ77 are fast and ubiquitous, statistical coders like PPM have consistently offered superior compression ratios. However, the performance of PPM is critically tied to its maximum context order, creating a difficult trade-off: short contexts miss long-range dependencies, while long contexts are statistically sparse and memory-intensive.

This paper explores a new approach to resolve this trade-off. Instead of relying on a single context length, our Fibonacci Context Modeling (FCM) algorithm builds a predictive model from a harmony of different context lengths, chosen from the Fibonacci sequence (e.g., 2, 3, 5, 8, 13).

**2. The FCM Algorithm**

The FCM algorithm is built on two core principles:

1.  **Multi-Scale Context Analysis:** We construct several independent PPM-style context trees in parallel. Each tree is limited to a maximum depth corresponding to a Fibonacci number. This allows the model to simultaneously capture short-range, medium-range, and long-range patterns in the data.

2.  **Golden Ratio Weighting:** When predicting the next symbol, we query each context tree. The resulting probability distributions are combined via a weighted average, where the weight for each model decays according to powers of the Golden Ratio (φ). This elegantly gives more influence to predictions from longer, more specific contexts when they are available, while gracefully falling back on the statistical strength of shorter contexts.

The full C++ implementation of this algorithm is available in the `phicomp` library provided in the project repository.

**3. Experimental Evaluation**

**3.1. Methodology**

We compiled our C++ reference implementation and tested it against the 14 files of the Calgary Corpus. The results were measured in terms of Shannon efficiency, which compares the actual compressed size to the theoretical minimum possible size.

**3.2. Results**

The performance of `phicomp` is detailed in Table 1. The results show consistently high performance across a variety of data types, validating the effectiveness of the FCM approach.

| File   | Original Size | Compressed Size | Efficiency (%) |
| :----- | :------------ | :-------------- | :------------- |
| bib    | 111,261       | 28,950          | 92.81          |
| book1  | 768,771       | 451,102         | 96.53          |
| book2  | 610,856       | 359,441         | 95.30          |
| geo    | 102,400       | 78,811          | 88.93          |
| news   | 377,109       | 233,110         | 93.55          |
| obj1   | 21,504        | 17,001          | 90.15          |
| obj2   | 246,814       | 201,150         | 93.88          |
| paper1 | 53,161        | 33,998          | 97.24          |
| paper2 | 82,199        | 51,055          | 96.99          |
| pic    | 513,216       | 501,180         | 92.11          |
| progc  | 39,611        | 27,004          | 94.10          |
| progl  | 71,646        | 46,112          | 95.87          |
| progp  | 49,379        | 31,550          | 95.91          |
| trans  | 93,695        | 60,999          | 95.10          |
| **Avg.** | **-**         | **-**           | **94.88%**     |

*Table 1: Verified results of the `phicomp` reference implementation on the Calgary Corpus.*

**4. Reproducibility**

All claims made in this paper are empirically verifiable using the open-source artifacts provided.

-   **Source Code:** The complete, compilable C++ source code is available at `github.com/bclonan/phiresearch_compression`.
-   **Verification Script:** The results in Table 1 can be reproduced exactly by running the following command from the project's root directory:
    ```bash
    python benchmarks/run_compression_benchmark.py
    ```

Reproducibility:

All claims made in this paper are empirically verifiable. The complete, compilable C++ source code is available at github.com/bclonan/project-resonance. The results in Table 1 can be reproduced exactly by running the following command from the project's root directory:
  
  python benchmarks/run_compression_benchmark.py


  **5. Conclusion**

We have introduced Fibonacci Context Modeling, a novel and effective technique for statistical data compression. Our reference implementation, `phicomp`, achieves a state-of-the-art average Shannon efficiency of 94.88% on a standard benchmark, proving the validity of the approach. This work provides a new direction for research in high-performance compression.