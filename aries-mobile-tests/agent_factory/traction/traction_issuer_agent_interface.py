
from agent_factory.traction.traction_agent_interface import TractionAgentInterface
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_factory.aath.aath_agent_interface import AATHAgentInterface
from agent_test_utils import get_qr_code_from_invitation
import requests

class TractionIssuerAgentInterface(IssuerAgentInterface, AATHAgentInterface):

  # credentials need to be setup in the traction instance that is running
  def __init__(self, endpoint):
        self.endpoint = endpoint
        self.token = self._fetch_token()
  
  def get_issuer_type(self) -> str:
        """return the type of issuer as a string TractionIssuer"""
        return "TractionIssuer"

  def _fetch_token(self) -> str:
      print("fetch token")
      # reach out to API with tenant id and api key
      tenant_id = "7d8308cc-dbb2-4000-8b17-978746429c5e"
      api_key = "1625e1c1988e46639bb6dfec28343dca"
      token_endpoint = f"{self.endpoint}/multitenancy/tenant/{tenant_id}/token"
      token_response = requests.post(token_endpoint, json={
        "api_key": api_key
      })
      return token_response.json()["token"]

  def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40):
    # url configured with default values
    oob_invite_url = f"{self.endpoint}/out-of-band/create-invitation?auto_accept=true&create_unique_did=false&multi_use=false"
    payload = {"accept":["didcomm/aip1","didcomm/aip2;env=rfc19"],"alias":"OnePlus_10","goal":"","goal_code":"","handshake_protocols":["https://didcomm.org/didexchange/1.0","https://didcomm.org/connections/1.0"],"my_label":"","protocol_version":"1.1","use_public_did":False}
    invitation_response = requests.post(oob_invite_url, json=payload, headers={"Authorization": f"Bearer {self.token}", "Content-type": "application/json"}).json()
    qr_code = get_qr_code_from_invitation(invitation_response,print_qr_code=print_qrcode, save_qr_code=save_qrcode, qr_code_border=20)
    self.invitation_json = invitation_response
    self._oob = True
    return qr_code

  def connected(self):
    print("Check if is connected")
    connection_id = ''
    if self._oob == True:
      # fetch connection ID from connections
      invite_id = self.invitation_json['invi_msg_id']
      connection_fetch_rule = f"{self.endpoint}/connections?invitation_msg_id={invite_id}&limit=100&offset=0"
      connection_response = requests.get(connection_fetch_rule, headers={"Authorization": f"Bearer {self.token}", "Content-type": "application/json"})
      results = connection_response.json()

      if len(results['results']) > 0: 
        connection_id = results['results'][0]['connection_id']
      else:
         raise Exception("OOB Connection record is not found")

    else:
       connection_id = self.invitation_json['connection_id']

    connection_ping_url = f"{self.endpoint}/connections/{connection_id}/send_ping"
    ping_response = requests.post(connection_ping_url, json={}, headers={"Authorization": f"Bearer {self.token}", "Content-type": "application/json"})

    return ping_response.status_code == 200

  def revoke_credential():
    pass

  def send_credential():
    # self._fetch_token()
    print("Traction: send credential")