from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements-dev.txt", "r") as fp:
    requirements = fp.read().split('\n')

# import jsonschemacodegen._version as _version

setup(
    name="enviroplusmonitor",
    # version=_version.__version__,
    author="Philip Cutler",
    author_email="greenthegarden@gmail.com",
    description="Publish readings from an enviro+ pHat over MQTT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greenthegarden/enviroplus-monitor.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements
)
