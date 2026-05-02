from setuptools import setup, find_packages
from pathlib import Path


# Read requirements
def read_requirements(filename):
    path = Path(__file__).parent / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    return []


# Read version
def read_version():
    path = Path(__file__).parent / 'VERSION'
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "0.0.1"


setup(
    name="dolphin-antidetect",
    version=read_version(),
    description="Anti-Detect Browser для обхода browser fingerprinting и bot detection",
    author="flaptos",
    author_email="flaptos@github.com",
    url="https://github.com/flaptos/Dolphin-AntiDetect",
    license="MIT",
    
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    package_dir={"": "src"},
    package_data={
        "dolphin": ["config/*.yaml"],
    },
    
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "full": read_requirements("requirements-dev.txt") + ["docker-sdk>=0.1.0"],
    },
    
    entry_points={
        "console_scripts": [
            "dolphin-cli=dolphin.main:main",
            "dolphin=dolphin.main:main",
        ],
    },
    
    python_requires=">=3.8",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
    ],
    
    keywords="antidetect browser fingerprint selenium automation stealth bot",
    
    long_description=Path("README.md").read_text(encoding="utf-8") if Path("README.md").exists() else "",
    long_description_content_type="text/markdown",
)
