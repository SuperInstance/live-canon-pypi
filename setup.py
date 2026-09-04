"""setup.py — Live Canon PyPI package"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="quilt-live-canon",
    version="0.8.4",
    description="Live Canon — read the AI-Writings canon as a navigable cell fabric (5 operations: NAVIGATE, CONFLUENCE, LINEAGE, GHOST, TICK).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Casey Digennaro",
    author_email="superinstance@users.noreply.github.com",
    url="https://github.com/SuperInstance/quilt-live-canon",
    packages=find_packages(),
    python_requires=">=3.10",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
