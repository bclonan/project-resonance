# phiresearch_compression/__init__.py
__version__ = "1.0.1"
__author__ = "Bradley Clonan"

from .compressor import compress, decompress
from .utils import calculate_shannon_entropy, verify_efficiency
try: 
    from . import core_bindings  # expose for advanced usage
except ImportError:  # pragma: no cover
    core_bindings = None

__all__ = [
    'compress', 'decompress', 'calculate_shannon_entropy', 'verify_efficiency',
    'core_bindings', '__version__'
]