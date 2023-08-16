#!/bin/sh
mkdir -p package
pip install --target ./package .
cd package 
zip -r ../package.zip .
cd ..
zip package.zip lambda_function.py
aws --profile dataminded --region eu-west-1 lambda update-function-code --function-name rushildaya-test --zip-file fileb://package.zip
```

