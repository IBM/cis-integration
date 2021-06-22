from typing import Mapping
from setuptools import setup

# setting up custom cli commmand entry point
setup (
    name='main.py',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'cis-integration=main:main',
            'ci=main:main'
        ]
    }
)