import setuptools


def long_description():
    with open("README.md", "r") as file:
        return file.read()


setuptools.setup(
    name="bach",
    version="0.1.0",
    author="Alessio Sclocco",
    author_email="alessio@sclocco.eu",
    license="Apache 2.0",
    description="BACH is a script to automatically analyze videos of ants.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/isazi/bach",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
        "Environment :: GPU",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.7',
    install_requires=[
        "numpy>=1.19.2",
        "opencv_python>=4.5.1.48",
        "opencv-contrib-python>=4.5.1.48"
    ],
)
