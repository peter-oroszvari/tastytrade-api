from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tastytrade-api",
    version="0.6.1",
    author="Peter Oroszvari",
    author_email="peter@oroszvari.hu",
    description="A Python client for the Tastytrade API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peter-oroszvari/tastytrade-api",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",

    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        ""
    ],
)
