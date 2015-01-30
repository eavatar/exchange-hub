#!/bin/sh
echo $(pwd)
. env/dev/bin/activate; python pyinstdev/pyinstaller.py pack/package.spec --clean -y

cp pack/Dockerfile dist/
docker build -t eavatartech/hub dist


