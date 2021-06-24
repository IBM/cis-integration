#!/bin/bash
python3 pip3 install -r requirements.txt
python3 setup.py develop
python3 install_check.py