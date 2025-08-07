# phiresearch_compression/__init__.py
__version__ = "1.0.1"
__author__ = "Bradley Clonan"

from .compressor import compress, decompress
from .utils import calculate_shannon_entropy, verify_efficiency

__all__ = [
    'compress', 'decompress', 'calculate_shannon_entropy', 'verify_efficiency',
    '__version__'
]