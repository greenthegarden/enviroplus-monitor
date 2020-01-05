# Enviroplus Monitor

https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-plus

To run test suite use

```bash
pip install nox
nox
```

Ensure python3 is default using, for example,

```bash
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip2 1
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2
```

Run using

```bash
pip install -r requirements.txt
python -m enviroplusmonitor
```
