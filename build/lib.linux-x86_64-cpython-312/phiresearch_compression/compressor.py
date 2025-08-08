# phiresearch_compression/compressor.py
from typing import Union

# This imports the *real*, compiled C++ extension.
# The 'core_bindings.so' (or .pyd) file is created when you run 'pip install .'.
from . import core_bindings

def compress(data: Union[bytes, bytearray]) -> bytes:
    """
    Compresses data using the C++ Fibonacci Context Modeling core.
    This is a direct wrapper to the high-performance, adaptive implementation.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input data must be bytes or bytearray.")
    
    # The pybind11 wrapper automatically handles converting Python bytes
    # to a std::string and the result back to bytes.
    return core_bindings.compress_main(data)

def decompress(data: Union[bytes, bytearray]) -> bytes:
    """
    Decompresses data using the C++ core. This function calls the
    fully implemented adaptive decompressor.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input data must be bytes or bytearray.")
    
    # Call the C++ decompressor, which will raise a std::runtime_error on failure.
    return core_bindings.decompress_main(data)