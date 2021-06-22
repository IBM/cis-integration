from typing import Mapping
from setuptools import setup

# setting up custom cli commmand entry point
setup (
    name='main.py',
    version='0.0.1',
    packages=["src"],
    entry_points={
        'console_scripts': [
<<<<<<< HEAD:setup.py
            'cis-integration=src.main:main',
            'ci=src.main:main'
=======
<<<<<<< HEAD:src/setup.py
            'cis-integration=main:main',
            'ci=main:main'
=======
            'cis-integration=src.main:main'
>>>>>>> d36c043 (working dockerization):setup.py
>>>>>>> dea0e91 (working dockerization):src/setup.py
        ]
    }
)