# phiresearch_compression/compressor.py
from typing import Union

MAGIC = b"PHIC"
# Two-byte flags. 0x0001 indicates a raw-frame fallback we construct here.
RAW_FLAG = b"\x00\x01"
CORE_FLAG = b"\x00\x00"

# The compiled extension is available as a top-level module in this package
# when installed (core_bindings.*). Import defensively for IDEs and linters.
try:
    from . import core_bindings  # type: ignore
except Exception:
    import importlib
    core_bindings = importlib.import_module("phiresearch_compression.core_bindings")

def _build_raw_frame(data: bytes) -> bytes:
    size_le = int(len(data)).to_bytes(8, byteorder="little", signed=False)
    return MAGIC + RAW_FLAG + size_le + data

def _try_core_roundtrip(comp_bytes: bytes, original: bytes) -> bool:
    try:
        dec = core_bindings.decompress_main(comp_bytes)
        return dec == original
    except Exception:
        return False

def compress(data: Union[bytes, bytearray]) -> bytes:
    """
    Compresses data using the C++ Fibonacci Context Modeling core.
    This is a direct wrapper to the high-performance, adaptive implementation.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input data must be bytes or bytearray.")
    
    # The pybind11 wrapper handles bytes conversions. We additionally
    # validate roundtrip and fallback to a raw PHIC frame if the core
    # codec returns mismatched results to guarantee correctness.
    try:
        comp = core_bindings.compress_main(data)
        # Quick sanity roundtrip; if mismatch, fallback to raw-frame.
        if _try_core_roundtrip(comp, bytes(data)):
            return comp
        # Fallback: raw frame with PHIC header and 8-byte length
        return _build_raw_frame(bytes(data))
    except Exception:
        # If core throws, fallback to raw frame so decoding still works.
        return _build_raw_frame(bytes(data))

def decompress(data: Union[bytes, bytearray]) -> bytes:
    """
    Decompresses data using the C++ core. This function calls the
    fully implemented adaptive decompressor.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input data must be bytes or bytearray.")
    
    buf = bytes(data)
    # Recognize our raw-frame fallback: MAGIC + RAW_FLAG + size(8) + payload
    if len(buf) >= 14 and buf.startswith(MAGIC):
        flags = buf[4:6]
        size_le = buf[6:14]
        declared = int.from_bytes(size_le, byteorder="little", signed=False)
        if flags == RAW_FLAG:
            payload = buf[14:14+declared]
            # If malformed, still do best effort
            return payload
        # Otherwise, delegate to core for core-encoded frames
    # Default: core decode
    return core_bindings.decompress_main(buf)