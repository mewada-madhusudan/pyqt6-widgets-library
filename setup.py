"""
Setup script for PyQt6 Widgets Library.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyqt6-widgets-library",
    version="1.1.0",
    author="Madhusudan Mewada",
    author_email="madhusudanmewadamm@gmail.com",
    description="A collection of polished, reusable PyQt6 widgets for building desktop applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mewada-madhusudan/pyqt6-widgets-library",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-qt>=4.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "examples": [
            "Pillow>=9.0",  # For image handling in examples
        ],
    },
    entry_points={
        "console_scripts": [
            "pyqt6-widgets-demo=pyqt_widgets.examples.basic_examples:run_basic_examples",
            "pyqt6-cards-showcase=pyqt_widgets.examples.card_showcase:run_card_showcase",
        ],
    },
    include_package_data=True,
    package_data={
        "pyqt_widgets": ["*.md", "examples/*.py"],
    },
)