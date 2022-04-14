import os
import json
import requests
import os
from pathlib import Path

# Make these parameters on the script. 
local_latest_app_json_filename = ".github/workflows/bc_wallet/latest_app.json"
platform = "ios"
sl_region = "us-west-1"
sl_user = "oauth-sheldon.regular-32de4"
sl_key = "06ca1bec-977d-4b12-926d-ab5bf5eb3709"

def find_latest_app(resp_json, platfrom):
    latest_app = None
    for item in resp_json["items"]:
        if latest_app == None == None or item['upload_timestamp'] > latest_app['upload_timestamp']:
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
if os.stat(local_latest_app_json_filename).st_size != 0: # It's not new
    with open(local_latest_app_json_file) as infile:
        local_latest_app_file_json = json.load(infile)
        if latest_app_json['upload_timestamp'] > local_latest_app_file_json['upload_timestamp']:
            # Save the file
            with open(local_latest_app_json_filename, 'w') as outfile:
                #outfile.write(json.dumps(infile))
                json.dump(latest_app_json, outfile)
else: # It's new just use the latest app found
    with open(local_latest_app_json_filename, 'w') as outfile:
        json.dump(latest_app_json, outfile)

# maybe save it to a repo file and push. Then let the main test run workflow pick up that push and run the tests. 
# this will run once a day after midnight.
