"""
Wanggan GPS Python Library - Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wanggan-gps",
    version="1.0.0",
    author="Hélio Teixeira",
    author_email="your.email@example.com",  # Update with your email
    description="Python library for Wanggan GPS handheld locators (tested on D6E)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wanggan-gps-python",  # Update with your repo
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyserial>=3.5",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
        "gui": [
            "easygui>=0.98.0",
        ],
    },
    py_modules=["wanggan_gps"],
    keywords="gps handheld locator wanggan d6e d7 serial hardware gpx kml",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/wanggan-gps-python/issues",
        "Source": "https://github.com/yourusername/wanggan-gps-python",
        "Documentation": "https://github.com/yourusername/wanggan-gps-python/blob/main/README.md",
    },
)
