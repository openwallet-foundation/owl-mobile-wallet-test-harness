"""
Base Class for actual AATH agents
"""

from agent_factory.issuer_agent_interface import IssuerAgentInterface
import json
from agent_test_utils import get_qr_code_from_invitation
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected


class AATHAgentInterface():

    _oob = False
    name = str

    def create_invitation_util(self, oob=False, print_qrcode=False, save_qrcode=False):
        """create an invitation and return the json back to the caller """
        self._oob = oob
        if self._oob is True:
            data = {"use_public_did": False}
            (resp_status, resp_text) = agent_controller_POST(
                self.endpoint + "/agent/command/",
                "out-of-band",
                operation="send-invitation-message",
                data=data,
            )
        else:
            (resp_status, resp_text) = agent_controller_POST(
                self.endpoint + "/agent/command/", "connection", operation="create-invitation"
            )

        if resp_status != 200:
            raise Exception(
                f"Call to create connection invitation failed: {resp_status}; {resp_text}"
            )
        else:
            self.invitation_json = json.loads(resp_text)
            if "label" in self.invitation_json["invitation"]:
                self.name = self.invitation_json["invitation"]["label"]
            qrimage = get_qr_code_from_invitation(self.invitation_json, print_qrcode, save_qrcode)
            return qrimage

    def get_name(self):
        if self.name:
            return self.name
        else:
            raise Exception("Agent name not set")

    def connected_util(self):
        """return True/False indicating if this issuer is connected to the wallet holder """

        # If OOB then make a call to get the connection id from the webhook. 
        if self._oob == True:
            # Get the responders's connection id from the above request's response webhook in the backchannel
            invitation_id = self.invitation_json["invitation"]["@id"]
            (resp_status, resp_text) = agent_controller_GET(
                self.endpoint  + "/agent/response/", "did-exchange", id=invitation_id
            )
            if resp_status != 200:
                raise Exception(
                    f"Call get the connection id from the OOB connection failed: {resp_status}; {resp_text}"
                )
            else:
                resp_json = json.loads(resp_text)
                connection_id = resp_json["connection_id"]
                self.invitation_json["connection_id"] = connection_id
        else:
            connection_id = self.invitation_json['connection_id']
        return expected_agent_state(self.endpoint, "connection", connection_id, "complete", sleep_time=2.0)

