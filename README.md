# Enviroplus Monitor

https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus

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

Run using

```bash
pip install -r requirements.txt
python -m enviroplusmonitor
```

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