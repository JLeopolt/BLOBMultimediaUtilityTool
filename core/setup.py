import core
from setuptools import setup, find_packages

setup(
    version=core.__version__,

    name="PyTube",
    description="Youtube converter library.",
    packages=find_packages(),
    install_requires=['pytube']
)
