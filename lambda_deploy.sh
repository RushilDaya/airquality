#!/bin/sh
mkdir -p package
rm -rf package
rm -rf build
rm -rf aq.egg-info
rm package.zip
mkdir -p package
pip install --force-reinstall --target ./package .
cd package 
zip -r ../package.zip .
cd ..
zip package.zip lambda_function.py
cp package.zip /mnt/c/Users/rushild/Desktop/package.zip # replace with direct deploy later on
