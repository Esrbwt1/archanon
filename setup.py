# setup.py

from setuptools import setup, find_packages

setup(
    name="archanon",
    version="0.1.0",
    author="[Your Name Here]", # Change this to your name or GitHub handle
    description="An open, safety-first research project for AGI.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "networkx",
        "datasets",
        "spacy>=3.0.0",
        # We will add other dependencies here as the project grows
    ],
    extras_require={
        "test": ["pytest"],
    }
)