#!/bin/env python3

import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="impo-haztecaso", # Replace with your own username
    version="0.0.1",
    author="Adrián Lattes",
    author_email="adrianlattes@disroot.org",
    description="todo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.haztecaso.com/impo",
    packages=setuptools.find_packages(),
    entry_points={ "console_scripts": ["impo = impo.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.6',
)

