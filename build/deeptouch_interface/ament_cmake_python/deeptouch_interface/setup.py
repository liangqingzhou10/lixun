from setuptools import find_packages
from setuptools import setup

setup(
    name='deeptouch_interface',
    version='0.0.0',
    packages=find_packages(
        include=('deeptouch_interface', 'deeptouch_interface.*')),
)
