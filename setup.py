"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("requirements-dev.txt", "r") as fp:
    requirements = fp.read().split('\n')

setup(
    name="enviroplusmonitor",
    version='0.0.1',
    description="Publish readings from an enviro+ pHat over MQTT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greenthegarden/enviroplus-monitor.git",
    author="Philip Cutler",
    author_email="greenthegarden@gmail.com",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'enviroplusmonitor'},
    packages=find_packages(where='enviroplusmonitor'),
    python_requires='>=3.7',
    install_requires=requirements,
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
)
