import sys
from os import path
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext as _build_ext

# --- Read the README for the long description ---
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Helper class to lazily find pybind11 include directory
class get_pybind_include:
    def __str__(self):
        import pybind11
        return pybind11.get_include()

# --- Define C++ Compiler Flags ---
extra_compile_args = []
if sys.platform == 'win32':
    # For MSVC on Windows, explicitly enable C++17 and OpenMP.
    extra_compile_args = ['/std:c++17', '/O2', '/openmp']
else:
    # For GCC/Clang on Linux/macOS
    extra_compile_args = ['-std=c++17', '-O3', '-fopenmp']

ext_modules = [
    Extension(
        'phiresearch_compression.core_bindings',
        ['resonance/phiresearch_compression/core/fcm_core.cpp'],
        include_dirs=[str(get_pybind_include())],
        language='c++',
        extra_compile_args=extra_compile_args,
        extra_link_args=['-fopenmp'] if sys.platform != 'win32' else ['/openmp']
    ),
]

class build_ext(_build_ext):
    """A custom build extension to add compiler-specific flags."""
    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = []
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args.extend(opts)
        _build_ext.build_extensions(self)

setup(
    name='project-resonance',
    version='1.0.1',
    author='Bradley Clonan',
    description='A collection of high-performance system components based on mathematical coherence.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'resonance'},
    packages=find_packages(where='resonance'),
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
    python_requires='>=3.8',
    setup_requires=['pybind11>=2.6'],
    install_requires=['pybind11>=2.6'],
    extras_require={
        "benchmark": ["requests", "tabulate", "fastapi", "uvicorn[standard]"],
    }
)