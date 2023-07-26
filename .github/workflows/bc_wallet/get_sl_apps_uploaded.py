from ast import Raise
import os
import json
import requests
import os
import sys
from pathlib import Path

# exit if not enough arguments passed to script
if len(sys.argv) != 6: 
    raise Exception(
        "Incorrect argument passed to script. Usage: python .github/workflows/bc_wallet/get_sl_apps_uploaded.py <Sauce Labs User> <Suace Labs Key> <Platform> <Sauce Labs Region> <Latest App File eg .github/workflows/bc_wallet/latest_app.json>"
        )

# Assign script parameters
sl_user = sys.argv[1]
sl_key = sys.argv[2]
platform = sys.argv[3]
sl_region = sys.argv[4]
local_latest_app_json_filename = sys.argv[5]


def find_latest_app(resp_json, platfrom):
    latest_app = None
    for item in resp_json["items"]:
        if latest_app == None or item['upload_timestamp'] > latest_app['upload_timestamp']:
            latest_app = item
    return latest_app

# call api to get app json
resp = requests.get(f'https://api.{sl_region}.saucelabs.com/v1/storage/files', auth=(sl_user, sl_key))
resp_json = resp.json()

# traverse app json to get the lastest upload_timestamp for the platform(kind)
if resp.status_code == 200:
    latest_app_json = find_latest_app(resp_json, platform)
else:
    raise Exception(f"There was a problem getting the list of available apps in Sauce Labs: {resp_json}")

local_latest_app_json_file = Path(local_latest_app_json_filename)
local_latest_app_json_file.touch(exist_ok=True)
if os.stat(local_latest_app_json_filename).st_size != 0: # Local json file is not new
    with open(local_latest_app_json_file) as infile:
        local_latest_app_file_json = json.load(infile)
        if latest_app_json['upload_timestamp'] > local_latest_app_file_json['upload_timestamp']:
            # Save the file
            with open(local_latest_app_json_filename, 'w') as outfile:
                #outfile.write(json.dumps(infile))
                print('true')
                file_name, ext = os.path.splitext(latest_app_json['name'])
                print(file_name)
                json.dump(latest_app_json, outfile)
        else:
            print('false')
else: # Local json file is new, just use the latest app found
    with open(local_latest_app_json_filename, 'w') as outfile:
        print('true')
        file_name, ext = os.path.splitext(latest_app_json['name'])
        print(file_name)
        json.dump(latest_app_json, outfile)
