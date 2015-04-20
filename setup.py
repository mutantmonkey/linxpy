from setuptools import setup
from linx import __version__

setup(
    name="linxpy",
    version=__version__,
    py_modules=["linx"],
    entry_points={
        "console_scripts": [
            "linx = linx:linx",
            "unlinx = linx:unlinx",
        ],
    },
    install_requires=["requests>=2.4"],
    description="A Python client for linx.li.",
    license="WTFPL",
    author="mutantmonkey",
    author_email="linxpy@mutantmonkey.in",
    keywords="linx linxpy upload",
    url="https://github.com/mutantmonkey/linxpy"
)
