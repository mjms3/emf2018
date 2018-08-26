mkdir -p /tmp/dist
cp  -rf ../* /tmp/dist
cp -rf $VIRTUAL_ENV/lib/python3.7/site-packages/* /tmp/dist
zip -r /tmp/deploy.zip /tmp/dist
aws s3 cp /tmp/deploy.zip s3://emf2018-server
aws lambda update-function-code --function-name create_user --s3-bucket emf2018-server --s3-key deploy.zip --publish
