from setuptools import Extension, setup
from Cython.Build import cythonize

ext = Extension(
    "cydiv",
    ["cydiv.pyx"],
    extra_compile_args=["-O2", "-fopenmp"],
    extra_link_args=["-fopenmp"],
)

setup(ext_modules=cythonize(ext, language_level="3"))
