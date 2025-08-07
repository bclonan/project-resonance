import sys
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as _build_ext

# Helper class to lazily find pybind11 include directory
class get_pybind_include:
    def __str__(self):
        import pybind11
        return pybind11.get_include()

# --- Define C++ Compiler Flags ---
extra_compile_args = []
if sys.platform == 'win32':
    extra_compile_args = ['/std:c++17', '/O2', '/openmp']
else:
    extra_compile_args = ['-std=c++17', '-O3', '-fopenmp']

ext_modules = [
    Extension(
        'phiresearch_compression.core_bindings',
        ['phiresearch_compression/core/fcm_core.cpp'],
        include_dirs=[get_pybind_include()],
        language='c++',
        extra_compile_args=extra_compile_args,
        extra_link_args=['-fopenmp'] if sys.platform != 'win32' else ['/openmp']
    ),
]

# The setup() function is now much simpler. All metadata is in pyproject.toml.
setup(
    packages=find_packages(),
    ext_modules=ext_modules,
    zip_safe=False,
)