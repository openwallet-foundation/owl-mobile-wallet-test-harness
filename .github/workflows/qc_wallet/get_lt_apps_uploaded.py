from ast import Raise
import os
import json
import requests
import os
import sys
from pathlib import Path

# exit if not enough arguments passed to script
if len(sys.argv) != 5: 
    raise Exception(
        "Incorrect argument passed to script. Usage: python .github/workflows/qc_wallet/get_lt_apps_uploaded.py <LambdaTest User> <LambdaTest Key> <Platform> <Latest App File eg .github/workflows/qc_wallet/latest_app.json>"
        )

# Assign script parameters
lt_user = sys.argv[1]
lt_key = sys.argv[2]
platform = sys.argv[3]
local_latest_app_json_filename = sys.argv[4]


def find_latest_app(resp_json):
    latest_app = None
    for item in resp_json['data']:
        if latest_app == None or item['updated_at'] > latest_app['updated_at']:
            latest_app = item
    return latest_app

# call api to get app json
# https://sylvain.rousseau:3nWogJYioE3aW7EwVO5b1xSqLdcALtfjTQOXt1wYLxg7UUo5tr@manual-api.lambdatest.com/app/data?type=android&level=user
resp = requests.get(f'https://%s:%s@manual-api.lambdatest.com/app/data?type=%s&level=user' % (
                        lt_user, lt_key, platform.lower()))
resp_json = resp.json()

# traverse app json to get the lastest upload_timestamp for the platform(kind)
if resp.status_code == 200:
    latest_app_json = find_latest_app(resp_json)
else:
    raise Exception(f"There was a problem getting the list of available apps in LambdaTest: {resp_json}")

local_latest_app_json_file = Path(local_latest_app_json_filename)
local_latest_app_json_file.touch(exist_ok=True)
if os.stat(local_latest_app_json_filename).st_size != 0: # Local json file is not new
    with open(local_latest_app_json_file) as infile:
        local_latest_app_file_json = json.load(infile)
        if latest_app_json['updated_at'] > local_latest_app_file_json['updated_at']:
            # Save the file
            with open(local_latest_app_json_filename, 'w') as outfile:
                #outfile.write(json.dumps(infile))
                print('true')
                app_url, ext = os.path.splitext(latest_app_json['app_id'])
                print(app_url)
                json.dump(latest_app_json, outfile)
        else:
            print('false')
else: # Local json file is new, just use the latest app found
    with open(local_latest_app_json_filename, 'w') as outfile:
        print('true')
        file_name, ext = os.path.splitext(latest_app_json['name'])
        print(file_name)
        json.dump(latest_app_json, outfile)

