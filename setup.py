from setuptools import setup, find_packages

setup(
    name="nutty",
    author="vijaydeepbhatt",
    author_email="vijaydeepbhatt@gmail.com",
    description="Educational RISC-V CPU and SoC using Amaranth HDL",
    long_description="""Educational RISC-V CPU and SoC using Amaranth HDL. It passes RISC-V compliance tests. Could be used for further CPU designs such as pipelined
    implementation memory controller studies, or perhaps your own home automation fully open sourced  !!! """,
    license="BSD",
    setup_requires=["wheel", "setuptools", "setuptools_scm"],
    install_requires=[
        "importlib_metadata",
    ],
    packages=find_packages(),
)