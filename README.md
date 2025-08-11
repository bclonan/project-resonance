# Project Resonance

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status: Reference Implementation](https://img.shields.io/badge/status-reference_implementation-green)](./README.md#project-status)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](./README.md#getting-started-installation)

## Project Status: A High-Fidelity Reference Implementation

Project Resonance is a functional, high-fidelity reference implementation of the concepts in our papers. It provides a complete, verifiable blueprint backed by real C++ code and measurable benchmarks.

## The Core Philosophy: Mathematical Coherence

We unify core components on a single mathematical foundation—algorithms derived from the Golden Ratio (φ)—to produce emergent performance characteristics that exceed the sum of parts.

## Key Achievements

1. **Novel Compression (`phicomp`)**
   - C++-backed Fibonacci Context Modeling (FCM)
   - Reproducible Calgary Corpus results, ~94.88% of Shannon limit

1. **System Throughput Validation**
   - Containerized benchmark shows ~1.82x throughput vs a traditional Nginx stack

1. **Complete Research Artifact**
   - Papers, C++ reference implementation, automated benchmarks

## Interactive 3D: Golden Ratio Model (φ)

GitHub renders ASCII STL inline. The model shows a thin golden rectangle: a 1×1 square (left) plus a 1×(φ−1) (~0.618) rectangle (right).

```stl
solid phi_square
  facet normal 0 0 1
    outer loop
      vertex 0.0 0.0 0.05
      vertex 1.0 0.0 0.05
      vertex 1.0 1.0 0.05
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0.0 0.0 0.05
      vertex 1.0 1.0 0.05
      vertex 0.0 1.0 0.05
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0.0 0.0 0.0
      vertex 1.0 1.0 0.0
      vertex 1.0 0.0 0.0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0.0 0.0 0.0
      vertex 0.0 1.0 0.0
      vertex 1.0 1.0 0.0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 0.0 0.0 0.05
      vertex 0.0 1.0 0.05
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 0.0 1.0 0.05
      vertex 0.0 1.0 0.0
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.0 1.0 0.05
      vertex 1.0 0.0 0.05
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.0 1.0 0.0
      vertex 1.0 1.0 0.05
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 1.0 0.0 0.05
      vertex 1.0 0.0 0.0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0.0 0.0 0.0
      vertex 0.0 0.0 0.05
      vertex 1.0 0.0 0.05
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0.0 1.0 0.0
      vertex 1.0 1.0 0.0
      vertex 1.0 1.0 0.05
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0.0 1.0 0.0
      vertex 1.0 1.0 0.05
      vertex 0.0 1.0 0.05
    endloop
  endfacet
endsolid

solid phi_minor_rect
  facet normal 0 0 1
    outer loop
      vertex 1.0 0.0 0.05
      vertex 1.6180339 0.0 0.05
      vertex 1.6180339 1.0 0.05
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 1.0 0.0 0.05
      vertex 1.6180339 1.0 0.05
      vertex 1.0 1.0 0.05
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.6180339 1.0 0.0
      vertex 1.6180339 0.0 0.0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.0 1.0 0.0
      vertex 1.6180339 1.0 0.0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.0 0.0 0.05
      vertex 1.0 1.0 0.05
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.0 1.0 0.05
      vertex 1.0 1.0 0.0
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1.6180339 0.0 0.0
      vertex 1.6180339 1.0 0.05
      vertex 1.6180339 0.0 0.05
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1.6180339 0.0 0.0
      vertex 1.6180339 1.0 0.0
      vertex 1.6180339 1.0 0.05
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.6180339 0.0 0.05
      vertex 1.6180339 0.0 0.0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 1.0 0.0 0.0
      vertex 1.0 0.0 0.05
      vertex 1.6180339 0.0 0.05
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 1.0 1.0 0.0
      vertex 1.6180339 1.0 0.0
      vertex 1.6180339 1.0 0.05
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 1.0 1.0 0.0
      vertex 1.6180339 1.0 0.05
      vertex 1.0 1.0 0.05
    endloop
  endfacet
endsolid
```

**Fibonacci tiling** (1, 1, 2, 3) as stepped plates with proportional heights (0.1, 0.1, 0.2, 0.3) to suggest “evolving layers” and compression over time. It’s manifold enough for GitHub’s 3D viewer and small enough to keep the README snappy.

```stl
solid fibonacci_steps
  // Square A: 1x1 at (0,0)–(1,1), height 0.1
  facet normal 0 0 1
    outer loop
      vertex 0 0 0.1
      vertex 1 0 0.1
      vertex 1 1 0.1
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0 0 0.1
      vertex 1 1 0.1
      vertex 0 1 0.1
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 1 0
      vertex 1 1 0
      vertex 1 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 1 0
      vertex 1 0 0
      vertex 0 0 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 1 0
      vertex 0 1 0.1
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 1 0.1
      vertex 0 0 0.1
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 0 0.1
      vertex 1 1 0.1
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 1 0.1
      vertex 1 1 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 0 0 0.1
      vertex 1 0 0.1
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 1 0 0.1
      vertex 1 0 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 1 0
      vertex 1 1 0
      vertex 1 1 0.1
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 1 0
      vertex 1 1 0.1
      vertex 0 1 0.1
    endloop
  endfacet

  // Square B: 1x1 at (1,0)–(2,1), height 0.1
  facet normal 0 0 1
    outer loop
      vertex 1 0 0.1
      vertex 2 0 0.1
      vertex 2 1 0.1
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 1 0 0.1
      vertex 2 1 0.1
      vertex 1 1 0.1
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 1 1 0
      vertex 2 1 0
      vertex 2 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 1 1 0
      vertex 2 0 0
      vertex 1 0 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 1 0
      vertex 1 1 0.1
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 1 0.1
      vertex 1 0 0.1
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 0 0
      vertex 2 0 0.1
      vertex 2 1 0.1
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 0 0
      vertex 2 1 0.1
      vertex 2 1 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 1 0 0
      vertex 1 0 0.1
      vertex 2 0 0.1
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 1 0 0
      vertex 2 0 0.1
      vertex 2 0 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 1 1 0
      vertex 2 1 0
      vertex 2 1 0.1
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 1 1 0
      vertex 2 1 0.1
      vertex 1 1 0.1
    endloop
  endfacet

  // Square C: 2x2 at (0,1)–(2,3), height 0.2
  facet normal 0 0 1
    outer loop
      vertex 0 1 0.2
      vertex 2 1 0.2
      vertex 2 3 0.2
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0 1 0.2
      vertex 2 3 0.2
      vertex 0 3 0.2
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 3 0
      vertex 2 3 0
      vertex 2 1 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 3 0
      vertex 2 1 0
      vertex 0 1 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 1 0
      vertex 0 3 0
      vertex 0 3 0.2
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 1 0
      vertex 0 3 0.2
      vertex 0 1 0.2
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 1 0
      vertex 2 1 0.2
      vertex 2 3 0.2
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 1 0
      vertex 2 3 0.2
      vertex 2 3 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 1 0
      vertex 0 1 0.2
      vertex 2 1 0.2
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 1 0
      vertex 2 1 0.2
      vertex 2 1 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 3 0
      vertex 2 3 0
      vertex 2 3 0.2
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 3 0
      vertex 2 3 0.2
      vertex 0 3 0.2
    endloop
  endfacet

  // Square D: 3x3 at (-3,0)–(0,3), height 0.3
  facet normal 0 0 1
    outer loop
      vertex -3 0 0.3
      vertex 0 0 0.3
      vertex 0 3 0.3
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex -3 0 0.3
      vertex 0 3 0.3
      vertex -3 3 0.3
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex -3 3 0
      vertex 0 3 0
      vertex 0 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex -3 3 0
      vertex 0 0 0
      vertex -3 0 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -3 0 0
      vertex -3 3 0
      vertex -3 3 0.3
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -3 0 0
      vertex -3 3 0.3
      vertex -3 0 0.3
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 0 0.3
      vertex 0 3 0.3
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 3 0.3
      vertex 0 3 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -3 0 0
      vertex -3 0 0.3
      vertex 0 0 0.3
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -3 0 0
      vertex 0 0 0.3
      vertex 0 0 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex -3 3 0
      vertex 0 3 0
      vertex 0 3 0.3
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex -3 3 0
      vertex 0 3 0.3
      vertex -3 3 0.3
    endloop
  endfacet
endsolid
```

### Optional caption for the README

> *Fibonacci Tiling (1,1,2,3) as rising plates. Heights encode step weights, hinting at our evolving, layered compression: short cycles → stable bases → larger aggregates. The geometry mirrors our grid → RGBD memory → regeneration pipeline.*

**twisted triangular prism** (“Pisano Twist”) where the top is rotated **60°** relative to the base to echo the 60-step Pisano-cycle vibe. It reads visually as a low-poly helix—clean, tiny, and manifold for GitHub’s 3D viewer.

```stl
solid pisano_twist
  // Bottom triangle (z=0)
  facet normal 0 0 -1
    outer loop
      vertex 1.0 0.0 0.0
      vertex -0.5 0.8660254 0.0
      vertex -0.5 -0.8660254 0.0
    endloop
  endfacet

  // Top triangle (z=1) rotated +60°
  facet normal 0 0 1
    outer loop
      vertex 0.5 0.8660254 1.0
      vertex -1.0 0.0 1.0
      vertex 0.5 -0.8660254 1.0
    endloop
  endfacet

  // Side 1 (between edge B1->B2 and T1->T2)
  facet normal 0.4082483 0.7071067 0.5773503
    outer loop
      vertex 1.0 0.0 0.0
      vertex -0.5 0.8660254 0.0
      vertex -1.0 0.0 1.0
    endloop
  endfacet
  facet normal 0.8164966 -0.0 0.5773503
    outer loop
      vertex 1.0 0.0 0.0
      vertex -1.0 0.0 1.0
      vertex 0.5 0.8660254 1.0
    endloop
  endfacet

  // Side 2 (between edge B2->B3 and T2->T3)
  facet normal -0.4082483 0.7071067 0.5773503
    outer loop
      vertex -0.5 0.8660254 0.0
      vertex -0.5 -0.8660254 0.0
      vertex 0.5 -0.8660254 1.0
    endloop
  endfacet
  facet normal -0.8164966 0.0 0.5773503
    outer loop
      vertex -0.5 0.8660254 0.0
      vertex 0.5 -0.8660254 1.0
      vertex -1.0 0.0 1.0
    endloop
  endfacet

  // Side 3 (between edge B3->B1 and T3->T1)
  facet normal 0.0 -0.8164966 0.5773503
    outer loop
      vertex -0.5 -0.8660254 0.0
      vertex 1.0 0.0 0.0
      vertex 0.5 0.8660254 1.0
    endloop
  endfacet
  facet normal 0.4082483 -0.7071067 0.5773503
    outer loop
      vertex -0.5 -0.8660254 0.0
      vertex 0.5 0.8660254 1.0
      vertex 0.5 -0.8660254 1.0
    endloop
  endfacet
endsolid
```

the **third** micro-model: a **Fibonacci spiral ramp** (1, 1, 2, 3, 5). It extends the tiling to the 5×5 square and uses increasing Z heights to suggest “growth → aggregation → regeneration.” Drop this under the other two in your README.

```stl
solid golden_spiral_ramp
  // S1: 1x1 at (0,0)-(1,1), height 0.12
  facet normal 0 0 1
    outer loop
      vertex 0 0 0.12
      vertex 1 0 0.12
      vertex 1 1 0.12
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0 0 0.12
      vertex 1 1 0.12
      vertex 0 1 0.12
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 1 0
      vertex 1 1 0
      vertex 1 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 1 0
      vertex 1 0 0
      vertex 0 0 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 1 0
      vertex 0 1 0.12
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 1 0.12
      vertex 0 0 0.12
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 0 0.12
      vertex 1 1 0.12
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 1 0.12
      vertex 1 1 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 0 0 0.12
      vertex 1 0 0.12
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 0 0
      vertex 1 0 0.12
      vertex 1 0 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 1 0
      vertex 1 1 0
      vertex 1 1 0.12
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 1 0
      vertex 1 1 0.12
      vertex 0 1 0.12
    endloop
  endfacet

  // S2: 1x1 at (1,0)-(2,1), height 0.15
  facet normal 0 0 1
    outer loop
      vertex 1 0 0.15
      vertex 2 0 0.15
      vertex 2 1 0.15
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 1 0 0.15
      vertex 2 1 0.15
      vertex 1 1 0.15
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 1 1 0
      vertex 2 1 0
      vertex 2 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 1 1 0
      vertex 2 0 0
      vertex 1 0 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 1 0
      vertex 1 1 0.15
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 1 0 0
      vertex 1 1 0.15
      vertex 1 0 0.15
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 0 0
      vertex 2 0 0.15
      vertex 2 1 0.15
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 0 0
      vertex 2 1 0.15
      vertex 2 1 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 1 0 0
      vertex 1 0 0.15
      vertex 2 0 0.15
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 1 0 0
      vertex 2 0 0.15
      vertex 2 0 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 1 1 0
      vertex 2 1 0
      vertex 2 1 0.15
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 1 1 0
      vertex 2 1 0.15
      vertex 1 1 0.15
    endloop
  endfacet

  // S3: 2x2 at (0,1)-(2,3), height 0.20
  facet normal 0 0 1
    outer loop
      vertex 0 1 0.20
      vertex 2 1 0.20
      vertex 2 3 0.20
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0 1 0.20
      vertex 2 3 0.20
      vertex 0 3 0.20
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 3 0
      vertex 2 3 0
      vertex 2 1 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0 3 0
      vertex 2 1 0
      vertex 0 1 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 1 0
      vertex 0 3 0
      vertex 0 3 0.20
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0 1 0
      vertex 0 3 0.20
      vertex 0 1 0.20
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 1 0
      vertex 2 1 0.20
      vertex 2 3 0.20
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 1 0
      vertex 2 3 0.20
      vertex 2 3 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 1 0
      vertex 0 1 0.20
      vertex 2 1 0.20
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0 1 0
      vertex 2 1 0.20
      vertex 2 1 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 3 0
      vertex 2 3 0
      vertex 2 3 0.20
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 0 3 0
      vertex 2 3 0.20
      vertex 0 3 0.20
    endloop
  endfacet

  // S4: 3x3 at (-3,0)-(0,3), height 0.26
  facet normal 0 0 1
    outer loop
      vertex -3 0 0.26
      vertex 0 0 0.26
      vertex 0 3 0.26
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex -3 0 0.26
      vertex 0 3 0.26
      vertex -3 3 0.26
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex -3 3 0
      vertex 0 3 0
      vertex 0 0 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex -3 3 0
      vertex 0 0 0
      vertex -3 0 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -3 0 0
      vertex -3 3 0
      vertex -3 3 0.26
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -3 0 0
      vertex -3 3 0.26
      vertex -3 0 0.26
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 0 0.26
      vertex 0 3 0.26
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 0 0 0
      vertex 0 3 0.26
      vertex 0 3 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -3 0 0
      vertex -3 0 0.26
      vertex 0 0 0.26
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -3 0 0
      vertex 0 0 0.26
      vertex 0 0 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex -3 3 0
      vertex 0 3 0
      vertex 0 3 0.26
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex -3 3 0
      vertex 0 3 0.26
      vertex -3 3 0.26
    endloop
  endfacet

  // S5: 5x5 at (-3,-5)-(2,0), height 0.34
  facet normal 0 0 1
    outer loop
      vertex -3 -5 0.34
      vertex 2 -5 0.34
      vertex 2 0 0.34
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex -3 -5 0.34
      vertex 2 0 0.34
      vertex -3 0 0.34
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex -3 0 0
      vertex 2 0 0
      vertex 2 -5 0
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex -3 0 0
      vertex 2 -5 0
      vertex -3 -5 0
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -3 -5 0
      vertex -3 0 0
      vertex -3 0 0.34
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -3 -5 0
      vertex -3 0 0.34
      vertex -3 -5 0.34
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 -5 0
      vertex 2 -5 0.34
      vertex 2 0 0.34
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2 -5 0
      vertex 2 0 0.34
      vertex 2 0 0
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -3 -5 0
      vertex -3 -5 0.34
      vertex 2 -5 0.34
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -3 -5 0
      vertex 2 -5 0.34
      vertex 2 -5 0
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex -3 0 0
      vertex 2 0 0
      vertex 2 0 0.34
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex -3 0 0
      vertex 2 0 0.34
      vertex -3 0 0.34
    endloop
  endfacet
endsolid
```


* *Fibonacci Steps:* layers that encode deterministic bases for regeneration.
* *Pisano Twist (Δθ = 60°):* compact “helix” hinting at cycle length and residues.
* *Spiral Ramp (1,1,2,3,5):* growth arc—each layer higher, showing aggregation in our compression pipeline.


### Tiny caption (optional)

> *Pisano Twist (Δθ = 60°): a compact “helix” evoking the 60-step Pisano cycle. Use alongside the Fibonacci steps model to show layers (steps) + cycle (twist)—aka your evolving compression story.*


## Getting Started: Installation & Verification

You can compile the C++ core and run the verification benchmarks.

### Prerequisites

- Python 3.8+
- A C++17 compliant compiler (GCC, Clang, or MSVC Build Tools)
- `pip` and `setuptools`
- `pybind11`
- Docker and Docker Compose

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/bclonan/project-resonance.git
cd project-resonance

# 2. Install the libraries and their C++ bindings
pip install .
```

### Running the Demonstrations

1. **Verify the Compression Algorithm:**

```bash
python benchmarks/run_compression_benchmark.py
```

1. **Verify the System Resonance Effect:**

```bash
python system/run_system_benchmark.py
```

1. **Reflection Compression Demo (phicomp vs gzip baseline)**

Run the FastAPI demo server and open the Reflection UI:

```bash
uvicorn resonance_demos.app:app --reload
```

Visit `http://127.0.0.1:8000/demo/reflection` to:

- List local `/data` files
- Compress (phicomp) and view gzip baseline metrics
- Fetch & compress a public GitHub raw file
- Decode or download reconstructed originals (hash-verified)

Automated test coverage for the reflection endpoints:

```bash
pytest -q tests/test_reflection_demo.py
```

## Author & Contact Information

This project was created and is led by **Bradley Clonan**.

I’m a software engineer focused on high-performance computing, systems architecture, and applying mathematical ideas to real systems. This repo demonstrates C++, Python, algorithm design, and rigorous systems testing.

- Email: `clonanxyz@gmail.com`
- GitHub: [github.com/bclonan](https://github.com/bclonan)

## License

Apache License 2.0. See [LICENSE](LICENSE).
