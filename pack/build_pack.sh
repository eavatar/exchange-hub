#!/bin/sh
echo $(pwd)
python pyinstdev/pyinstaller.py pack/package.spec --clean -y


