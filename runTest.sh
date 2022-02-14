#!/bin/bash

#INFO: PARSING
#INFO: required programs (you will thank me later) bat, rg, fzf 
CLEAR='\033[0m'
RED='\033[0;31m'

function usage() {
  if [ -n "$1" ]; then
    echo -e "${RED}👉 $1${CLEAR}\n";
  fi
  echo "Usage: $0 [-u upload-app]"
  echo "  -u, --upload-app         Upload app to sauceLab"
  echo "  -f, --fzf                Select the test or group of test you want to run (Yo must indicate the subfolder e.g. ODS, bc_wallet)"
  echo "  -v, --verbose            All the command prompts"
  echo ""
  exit 1
}

# parse params
while [[ "$#" -gt 0 ]]; do case $1 in
  -u|--upload-app ) UPLOAD_FLAG=1;shift;shift;;
  -f|--fzf ) FZF="$2";shift;shift;; # if empty should ls the feature folder
  -v|--verbose) VERBOSE=1;shift;;
  *) usage "Unknown parameter passed: $1"; shift; shift;;
esac; done

# we store all the passwords in the local .env file
echo -e '\n=> Exporting secrets'
if [ -f .env ]
then
  source .env
else
  echo -e '\n=> No env file found abborting operation'
  echo "Missing .env file!" > logfile.log
  echo -e '\n=> Done'
  exit 125
fi
echo -e '\n=> Done'

if [ "$UPLOAD_FLAG" == 1 ]
then 
  echo -e '\n=> uploading the app'
  ./upload_app_to_SL.sh $DEVICE_CLOUD_USERNAME $DEVICE_CLOUD_ACCESS_KEY $APP_APK_LOCATION "ODS app" api.us-west-1
  echo -e '\n=> Done'
fi

if [ -n "$FZF" ]
then
  # TODO: using regex and ripgrep use this regex ^@\S+
  # echo -e $PWD/aries-mobile-tests/features/"$FZF"/availableTests.txt
  # echo $FZF
  SELECTED_TEST=$(bat $PWD/aries-mobile-tests/features/"$FZF"/availableTests.txt | fzf | rg -e '(@[^\s]+)' -o ) 
  
  echo -e "Selected the following tests: $SELECTED_TEST"
  echo -e '\n=> Done'
fi

echo -e '\n=> Removing all Dangling images'
docker rmi "$(docker images --filter "dangling=true" -q --no-trunc)"
echo -e '\n=> Done'

echo -e '\n=> Clean build'
./manage build -w ODS -i acapy-main -v acapy-main
echo -e '\n=> Done'

echo -e '\n=> Starting the saucy tests'
LEDGER_URL_CONFIG=http://test.bcovrin.vonx.io REGION=us-west-1 ./manage run -d SauceLabs -u $DEVICE_CLOUD_USERNAME -k $DEVICE_CLOUD_ACCESS_KEY -p Android -a $APP_NAME.apk -i acapy-main -v acapy-main -t $SELECTED_TEST
# NOTE: replace @connect with your feature file
echo -e '\n=> Done'

