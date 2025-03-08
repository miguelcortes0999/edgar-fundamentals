from setuptools import setup, find_packages

setup(
    name="edgar_fundamentals",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
    ],
    python_requires=">=3.0",
)

# pip install -e .