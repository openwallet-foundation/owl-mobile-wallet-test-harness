
from agent_test_utils import get_qr_code_from_invitation
import requests

class TractionAgentInterface():
  _oob = False
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
    tenant_id = "ac071379-7b24-4275-83d4-c6cc3b62701f"
    api_key = "60b75d3e9cf34fb3a46ae9d8b6cdf169"
    token_endpoint = f"{self.endpoint}/multitenancy/tenant/{tenant_id}/token"
    token_response = requests.post(token_endpoint, json={"api_key": api_key})
    if token_response.status_code != 200:
      raise Exception("Issue fetching token from Traction Agent, check tenant for connectivity.")
    return token_response.json()["token"]

  def create_invitation_util(self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40):
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
    invitation_response = requests.post(
        oob_invite_url, json=payload, headers=self._build_headers()
    ).json()

    qr_code = get_qr_code_from_invitation(
        invitation_response,
        print_qr_code=print_qrcode,
        save_qr_code=save_qrcode,
        qr_code_border=qr_code_border,
    )
    self.invitation_json = invitation_response
    self._oob = True
    return qr_code
    
