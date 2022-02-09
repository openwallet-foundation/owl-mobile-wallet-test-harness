#!/bin/bash
# we store all the passwords in the local .env file
export "$(cat .env | xargs)"
# removing all dangling images
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
# clean build
./manage build -w ODS -i acapy-main -v acapy-main
# testing
LEDGER_URL_CONFIG=http://test.bcovrin.vonx.io REGION=us-west-1 ./manage run -d SauceLabs -u $DEVICE_CLOUD_USERNAME -k $DEVICE_CLOUD_ACCESS_KEY -p Android -a app-release.apk -i acapy-main -v acapy-main -t @Connect


