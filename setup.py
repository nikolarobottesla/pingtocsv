# setup.py
'''
Setup tools
'''
import platform
import re
import subprocess
from setuptools import setup, find_packages

NAME = 'pingtocsv'
VERSION = '0.2.0'
LICENSE = 'MIT'
AUTHOR = 'Milo Oien-Rochat'
AUTHOR_EMAIL = 'nikolarobottesla@github.com'
DESCRIPTION = 'ping periodically log to csv'
URL = 'https://github.com/nikolarobottesla/pingtocsv'
DOWNLOAD_URL = ''

REQUIRES = [
    'pingparsing',
]

REQUIRES_TEST = [
    'pyinstaller',
]

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
]

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

def has_ssh() -> bool:
    """
    Check that the user has ssh access to github.mmm.com
    First it will verify if ssh is installed in $PATH
    then check if we can authenticate to github.mmm.com
    over ssh. Returns false if either of these are untrue
    """
    result = None
    if 'windows' in platform.platform().lower():
        ssh_test = subprocess.run(['where', 'ssh'])
    else:
        ssh_test = subprocess.run(['which', 'ssh'])
    if ssh_test.returncode == 0:
        result = subprocess.Popen(
            ['ssh', '-Tq', 'git@github.mmm.com', '&>', '/dev/null'])
        result.communicate()
    if not result or result.returncode == 255:
        return False
    return True

def flip_ssh(requires: list) -> list:
    '''
    Attempt to authenticate with ssh to github.com
    If permission is denied then flip the ssh dependencies
    to https dependencies automatically.
    '''
    # Not authenticated via ssh. Change ssh to https dependencies
    if not has_ssh():
        requires = list(map(
            lambda x: re.sub(r'ssh://git@', 'https://', x), requires
        ))
    return requires

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    download_url=DOWNLOAD_URL,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=flip_ssh(REQUIRES),
    extras_require={
        'dev': flip_ssh(REQUIRES_TEST),
    },
    entry_points={
        'console_scripts': [
            f'{NAME} = {NAME}:main',
        ]
    },
    include_package_data=True,
    python_requires='>=3.6'
)