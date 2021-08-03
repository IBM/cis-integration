#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/usr/local/bin
pip3 install -r requirements.txt
pip3 install -e . --target /usr/local/bin --upgrade
python3 install_check.py