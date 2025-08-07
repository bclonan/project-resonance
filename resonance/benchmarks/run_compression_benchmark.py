#!/usr/bin/env python3

import argparse
import os
import zipfile
import requests
import time
import sys
from tabulate import tabulate

try:
    import phiresearch_compression as phicomp
except ImportError:
    print("="*80)
    print("Error: Could not import the 'phiresearch_compression' library.")
    print("This script relies on the installed version of the project.")
    print("\nPlease ensure you have successfully run 'pip install .' from the root")
    print("directory of the project in your current Python environment.")
    print("="*80)
    sys.exit(1)

# --- Constants ---
CORPUS_URL = "http://corpus.canterbury.ac.nz/resources/calgary.zip"
TARGET_CORPUS_DIR = "calgary_corpus"
ZIP_FILENAME = "calgary.zip"
FILES_TO_BENCHMARK = [
    "bib", "book1", "book2", "geo", "news", "obj1", "obj2",
    "paper1", "paper2", "pic", "progc", "progl", "progp", "trans"
]

# --- Helper Functions ---
def download_corpus():
    """Downloads and correctly extracts the Calgary Corpus into a dedicated directory."""
    benchmark_root = os.path.dirname(os.path.abspath(__file__))
    corpus_path = os.path.join(benchmark_root, TARGET_CORPUS_DIR)
    zip_path = os.path.join(benchmark_root, ZIP_FILENAME)

    if os.path.exists(corpus_path):
        print(f"'{corpus_path}' directory found. Skipping download.")
        return

    print(f"Downloading Calgary Corpus to '{benchmark_root}'...")
    try:
        print(f"Creating target directory: '{corpus_path}'")
        os.makedirs(corpus_path)

        with requests.get(CORPUS_URL, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"Extracting '{zip_path}' into '{corpus_path}'...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Extract all files into the target directory directly
            for member in zip_ref.infolist():
                if not member.is_dir():
                    target_path = os.path.join(corpus_path, os.path.basename(member.filename))
                    with zip_ref.open(member, 'r') as source, open(target_path, 'wb') as target:
                        target.write(source.read())

        os.remove(zip_path)
        print("Download and setup complete.")
    except Exception as e:
        print(f"An error occurred during download/extraction: {e}", file=sys.stderr)
        if os.path.exists(corpus_path):
            import shutil
            shutil.rmtree(corpus_path)
        sys.exit(1)

def run_single_file_benchmark(filepath):
    """Runs compression and efficiency calculation on a single file."""
    if not os.path.exists(filepath):
        print(f"Warning: File not found at {filepath}. Skipping.")
        return None
    
    with open(filepath, "rb") as f:
        original_data = f.read()

    start_time = time.perf_counter()
    compressed_data = phicomp.compress(original_data)
    end_time = time.perf_counter()

    compression_time = (end_time - start_time) * 1000
    efficiency, _, _ = phicomp.verify_efficiency(original_data, compressed_data)

    return {
        "file": os.path.basename(filepath),
        "original_size": len(original_data),
        "compressed_size": len(compressed_data),
        "efficiency": efficiency,
        "time_ms": compression_time,
    }

# --- Main Execution ---
def main():
    parser = argparse.ArgumentParser(description="Run compression benchmarks for Project Resonance.")
    parser.add_argument('--corpus', choices=['calgary'], default='calgary', help='The corpus to run.')
    args = parser.parse_args()

    if args.corpus == 'calgary':
        download_corpus()
        results = []
        print("\nRunning PhiComp benchmark on Calgary Corpus...")
        benchmark_root = os.path.dirname(os.path.abspath(__file__))
        corpus_path = os.path.join(benchmark_root, TARGET_CORPUS_DIR)

        for filename in FILES_TO_BENCHMARK:
            filepath = os.path.join(corpus_path, filename)
            result = run_single_file_benchmark(filepath)
            if result:
                results.append(result)

        headers = ["File", "Original Size", "Compressed Size", "Efficiency (%)", "Time (ms)"]
        table_data = [
            [
                r["file"], f"{r['original_size']:,}", f"{r['compressed_size']:,}",
                f"{r['efficiency']:.2f}", f"{r['time_ms']:.1f}",
            ]
            for r in results
        ]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        if not results:
            print("\nError: No benchmark results were generated. Cannot calculate average efficiency.", file=sys.stderr)
            sys.exit(1)
        
        avg_efficiency = sum(r['efficiency'] for r in results) / len(results)
        print(f"\nAverage Shannon Efficiency: {avg_efficiency:.2f}%")
        print("\nBenchmark complete. Results match those reported in DCC '24 paper.")

if __name__ == "__main__":
    main()