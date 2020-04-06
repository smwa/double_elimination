import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="double_elimination",
    version="1.2.0",
    author="Michael Smith",
    author_email="michael.smith.ok@gmail.com",
    description="A double elimination tournament match handler.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smwa/double_elimination",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
