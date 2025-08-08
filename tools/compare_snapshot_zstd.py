#!/usr/bin/env python3
"""
Compare compression on a market snapshot ZIP downloaded from /api/market_snapshot.

Inputs:
  - path to market_snapshot_*.zip (contains raw.ndjson, phicomp.bin, gzip.bin, stats.json)

Outputs:
  - Prints sizes and computed savings vs raw for gzip, zstd, and phicomp (from snapshot)

Usage (PowerShell):
  python tools/compare_snapshot_zstd.py path/to/market_snapshot_10s.zip

Note: Requires the 'zstandard' Python package (optional).
"""
import json
import sys
import zipfile
import hashlib
try:
    import zstandard as zstd  # type: ignore
except Exception:
    zstd = None


def main(path: str) -> int:
    with zipfile.ZipFile(path, 'r') as zf:
        raw = zf.read('raw.ndjson')
        phicomp_bytes = zf.read('phicomp.bin')
        gzip_bytes = zf.read('gzip.bin')
        stats = json.loads(zf.read('stats.json').decode('utf-8'))
    # trust but verify
    sha = hashlib.sha256(raw).hexdigest()
    if sha != stats.get('sha256_raw'):
        print(f"WARNING: sha256 mismatch. stats={stats.get('sha256_raw')} actual={sha}")
    # recompress with zstd if available
    zstd_size = None
    if zstd is not None:
        cctx = zstd.ZstdCompressor(level=3)
        zstd_bytes = cctx.compress(raw)
        zstd_size = len(zstd_bytes)
    raw_sz = len(raw)
    phicomp_sz = len(phicomp_bytes)
    gzip_sz = len(gzip_bytes)
    print("Snapshot sizes (bytes):")
    print(f"  raw:      {raw_sz}")
    print(f"  gzip:     {gzip_sz}  (savings vs raw: {100.0 * (1 - gzip_sz/max(1,raw_sz)):.2f}%)")
    if zstd_size is not None:
        print(f"  zstd:     {zstd_size}  (savings vs raw: {100.0 * (1 - zstd_size/max(1,raw_sz)):.2f}%)")
    print(f"  phicomp:  {phicomp_sz}  (savings vs raw: {100.0 * (1 - phicomp_sz/max(1,raw_sz)):.2f}%)")
    if zstd_size is not None:
        rel = 100.0 * (1 - phicomp_sz/max(1, zstd_size))
        print(f"  phicomp vs zstd: {rel:.2f}%")
    rel_gz = 100.0 * (1 - phicomp_sz/max(1, gzip_sz))
    print(f"  phicomp vs gzip: {rel_gz:.2f}%")
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python tools/compare_snapshot_zstd.py path/to/market_snapshot_10s.zip")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
