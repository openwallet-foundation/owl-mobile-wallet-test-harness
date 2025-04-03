
from agent_test_utils import get_qr_code_from_invitation
import requests
import json

class TractionAgentInterface():
  _oob = False
  _connection_id = ""
  endpoint = ""
  token = ""
  invitation_json = {}

  def __init__(self, endpoint):
    print("Traction Agent Interface init")
    self.endpoint = endpoint
    self.token = self._fetch_token()
    self._schemas = {}
    self._credential_definitions = {}
    self._credential_json_dict = {}

  def _build_headers(self) -> dict[str, any]:
    return {
        "Authorization": f"Bearer {self.token}",
        "Content-type": "application/json",
    }

  def _fetch_token(self) -> str:
    print("fetch token")
    # reach out to API with tenant id and api key
    tenant_id = "487c5972-beed-4dec-8e18-b3316329e296"
    api_key = "0abaf514b5b845388b1aac9c2c138ffb"
    token_endpoint = f"{self.endpoint}/multitenancy/tenant/{tenant_id}/token"
    token_response = requests.post(token_endpoint, json={"api_key": api_key})
    if token_response.status_code != 200:
      raise Exception("Issue fetching token from Traction Agent, check tenant for connectivity.")
    return token_response.json()["token"]

  def create_invitation_util(self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40):
    self.token = self._fetch_token()
    print("Create OOB traction invitation")
    # url configured with default values
    oob_invite_url = f"{self.endpoint}/out-of-band/create-invitation?auto_accept=true&create_unique_did=false&multi_use=false"
    payload = {
        "accept": ["didcomm/aip1", "didcomm/aip2;env=rfc19"],
        "alias": "Sauce Labs Device",
        "goal": "",
        "goal_code": "",
        "handshake_protocols": [
            "https://didcomm.org/didexchange/1.0",
            "https://didcomm.org/connections/1.0",
        ],
        "my_label": "Sauce labs Connection",
        "protocol_version": "1.1",
        "use_public_did": False,
    }

    response = requests.post(
        oob_invite_url, json=payload, headers=self._build_headers()
    )
    
    if response.status_code != 200:
      raise Exception(f"Error creating invitation: {response.status_code}: {response.text}")
    
    
    self.invitation_json = response.json()
    self._oob = True

    qr_code = get_qr_code_from_invitation(
        invitation_json=self.invitation_json,
        print_qr_code=print_qrcode,
        save_qr_code=save_qrcode,
        qr_code_border=qr_code_border,
    )
    return qr_code
  
  def connected_util(self):
    connection_id = ""
    if self._oob:
        # fetch connection ID from connections
        invite_id = self.invitation_json["invi_msg_id"]
        connection_fetch_rule = f"{self.endpoint}/connections?invitation_msg_id={invite_id}&limit=100&offset=0"
        connection_response = requests.get(
            connection_fetch_rule, headers=self._build_headers()
        )
        results = connection_response.json()
        if results["results"]:
            connection_id = results["results"][0]["connection_id"]
        else:
            raise Exception("OOB Connection record is not found")

    else:
        connection_id = self.invitation_json["connection_id"]
    self._connection_id = connection_id
    connection_ping_url = f"{self.endpoint}/connections/{connection_id}/send-ping"
    ping_response = requests.post(
        connection_ping_url, json={}, headers=self._build_headers()
    )
    return ping_response.status_code == 200
    
