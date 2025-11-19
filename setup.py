"""
Setup configuration for nutshell package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from package
version = {}
with open("nutshell_pkg/__init__.py") as f:
    for line in f:
        if line.startswith("__version__"):
            exec(line, version)

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else ""

setup(
    name="nutshell",
    version=version["__version__"],
    description="Command-line tool for summarizing research papers using Claude API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['../Prompts/*.txt'],
    },
    data_files=[
        ('Prompts', ['Prompts/v1_baseline.txt', 'Prompts/v2_no_scratchpad.txt', 'Prompts/changelog.txt']),
    ],
    install_requires=[
        "anthropic>=0.40.0",
    ],
    entry_points={
        'console_scripts': [
            'nutshell=nutshell_pkg.cli:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
