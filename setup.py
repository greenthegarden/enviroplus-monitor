import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enviroplusmonitor", # Replace with your own username
    version="0.0.1",
    author="Philip Cutler",
    author_email="greenthegarden@gmail.com",
    description="Pubish readings from an enviro+ pHat over MQTT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greenthegarden/enviroplus-monitor.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
      'ads1015',
      'configobj',
      'enviroplus',
      'i2cdevice',
      'influxdb',
      'paho-mqtt',
      'pimoroni-bme280',
      'pint',
      'smbus',
      'timeloop',
    ]
)
