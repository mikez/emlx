from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="emlx",
    version="0.1.0",
    url="https://github.com/mikez/emlx",
    project_urls={
        "Code": "https://github.com/mikez/emlx",
        "Issue tracker": "https://github.com/mikez/emlx/issues",
    },
    license="MIT",
    author="Michael Belfrage",
    author_email="consulting@belfrage.net",
    description="The leightweight parser for emlx files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
