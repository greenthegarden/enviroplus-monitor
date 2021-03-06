# Enviroplus Monitor

https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus

## Requirements

```
sudo apt-get update
sudo apt-get upgrade
sudo apt install python3-dev python3-pip git
```

Ensure I2C interface is activated.

## Running

Ensure python3 is default using, for example,

```bash
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip2 1
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2
```

To run test suite use

```bash
pip install nox
nox
```

If using a [DHT22 sensor](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup) need to also run

```bash
sudo apt install libgpiod2
```

Run using

```bash
pip install -r requirements.txt
python -m enviroplusmonitor
```

## Debugging

To debug install. See https://medium.com/python-pandemonium/debugging-an-inactive-python-process-2b11f88730c7

```bash
sudo apt-get install gdb python3-dbg
```

To find process use

```bash
ps -ef | grep python
```

To run debugger use

```bash
gdb python process_id
```

At gdb prompt type `py-bt`.


## References:

* Continuous Integration: https://realpython.com/python-continuous-integration/
* pytest-docker-tools:
* https://hynek.me/talks/python-foss
* Testing in Python: https://realpython.com/python-testing/
* fake-rpi


#
* https://docs.pytest.org/en/latest/capture.html
* https://docs.pytest.org/en/latest/tmpdir.html
* https://docs.pytest.org/en/latest/fixture.html
* https://docs.pytest.org/en/latest/goodpractices.html

pytest.fixture
unittest.mock

## Run script as service

Add following to `/etc/systemd/system`, using `sudo cp enviroplusmonitor.service /etc/systemd/system`.

```bash
[Unit]
Description=Enviro+ Monitor
After=multi-user.target

[Service]
User=pi
Group=pi
WorkingDirectory=/home/pi/enviroplus-monitor
Type=simple
ExecStart=/usr/bin/python -m enviroplusmonitor
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Activate service using

```bash
sudo chmod 644 /etc/systemd/system/enviroplusmonitor.service
sudo systemctl daemon-reload
sudo systemctl enable enviroplusmonitor.service
sudo systemctl start enviroplusmonitor.service
```

### Check status

```bash
sudo systemctl status hello.service
```

### Start service

```bash
sudo systemctl start hello.service
```

### Stop service

```bash
sudo systemctl stop hello.service
```

### Check service's log

```bash
sudo journalctl -f -u hello.service
```


import platform
platform.node()

import socket
socket.gethostname()

# To run in background use

```bash
nohup python -m enviroplusmonitor > enviroplusmonitor.log &
```

To debug

```

Difficult to maintain consistency.service
Deviations in the topics
Deviations in the messages
AsyncAPI - single source of truth
Lack of tool support -

AsyncAPI Toolkit - Xtext and Eclipse.

Buiding AsyncAPI with Mercure protocol (new)
API Platform for WebAI
@dunglas
Les-Tilleuls.coop
EventSource protocol SSE (HTTP connection which remains open)
HTTP2 supports passing of data (websocket obsolete in HTTP2&3)
