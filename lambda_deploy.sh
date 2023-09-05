#!/bin/sh
set -e # exit on first error
pytest tests/
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
aws --profile dataminded --region eu-west-1 lambda update-function-code \
    --function-name  rushildaya-test \
    --zip-file fileb://package.zip