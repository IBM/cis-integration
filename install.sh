#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/usr/local/bin
pip3 install -r requirements.txt
python3 setup.py develop --install-dir /usr/local/bin
python3 install_check.py