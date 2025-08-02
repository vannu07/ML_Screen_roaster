#!/usr/bin/env python3
"""
Setup script for Screen Time Roast Analyzer package.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'docs', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Screen Time Roast Analyzer - ML-powered screen time analysis and roast generation"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="screen-time-roast-analyzer",
    version="1.0.0",
    author="AI/ML Engineer",
    author_email="contact@screenroaster.com",
    description="ML-powered screen time analysis and personalized roast generation system",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/screen-time-roast-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "api": [
            "google-generativeai>=0.3.0",
        ],
        "web": [
            "fastapi>=0.68.0",
            "uvicorn>=0.15.0",
            "streamlit>=1.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipykernel>=6.0.0",
            "plotly>=5.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "screen-roast-analyzer=main:main",
            "setup-screen-roast=scripts.setup_environment:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.csv", "*.json", "*.txt", "*.md"],
    },
    project_urls={
        "Bug Reports": "https://github.com/your-username/screen-time-roast-analyzer/issues",
        "Source": "https://github.com/your-username/screen-time-roast-analyzer",
        "Documentation": "https://github.com/your-username/screen-time-roast-analyzer/docs",
    },
)