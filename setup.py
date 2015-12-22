from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='adusk',
    version='',
    packages=[''],
    url='',
    license='GPL3',
    author='archshift',
    author_email='',
    description='',
    ext_modules=cythonize(["adusk.py"]),
)
