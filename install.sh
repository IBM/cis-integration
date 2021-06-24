#!/bin/bash
python3 pip3 install -r requirements.txt
python3 setup.py develop --prefix /usr/local/bin
python3 install_check.py