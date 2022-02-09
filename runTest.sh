#!/bin/bash

# we store all the passwords in the local .env file
echo -e '\n=> Exporting secrets'
if [ -f .env ]
then
  # export "$(cat .env | xargs)"
  source .env
  # echo $DEVICE_CLOUD_USERNAME 
else
  echo "Missing .env file!" > logfile.log
  exit 125
fi
echo -e '\n=> Done'

echo -e '\n=> uploading the app'
./upload_app_to_SL.sh $DEVICE_CLOUD_USERNAME $DEVICE_CLOUD_ACCESS_KEY /$APP_APK_LOCATION "Android Bifold ON App" api.us-west-1S
echo -e '\n=> Done'

echo -e '\n=> Removing all Dangling images'
docker rmi "$(docker images --filter "dangling=true" -q --no-trunc)"
echo -e '\n=> Done'

echo -e '\n=> Clean build'
./manage build -w ODS -i acapy-main -v acapy-main
echo -e '\n=> Done'

# testing
echo -e '\n=> Starting the saucy tests'
LEDGER_URL_CONFIG=http://test.bcovrin.vonx.io REGION=us-west-1 ./manage run -d SauceLabs -u $DEVICE_CLOUD_USERNAME -k $DEVICE_CLOUD_ACCESS_KEY -p Android -a app-release.apk -i acapy-main -v acapy-main -t @Connect
echo -e '\n=> Done'


