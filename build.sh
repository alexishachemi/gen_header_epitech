#!/bin/bash

pyinstaller -n gen_header --onefile *.py
rm -rf build
rm -rf __pycache__
mv dist/gen_header .
rm -rf dist
rm gen_header.spec