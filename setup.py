# Copyright (c) 2025 CungUng. All rights reserved.
# This setup.py is licensed for personal, non-commercial use only.
raise RuntimeError(
    "This version of flexbt is licensed for personal, non-commercial use only. "
    "Contact the author for commercial licensing."
)

from setuptools import setup, find_packages

setup(
    name="flexbt",
    version="0.1.0",
    description="A library for back-testing trading strategies",
    author="CungUng",
    author_email="milkywayy1511@gmail.com",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "numpy>=2.2.2",
        "pandas>=2.2.3",
        "python-dateutil>=2.9.0.post0",
        "pytz>=2025.1",
        "six>=1.17.0",
        "tzdata>=2025.1",
    ],
    python_requires=">=3.11",  # Based on the Python version shown in __pycache__ files
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
