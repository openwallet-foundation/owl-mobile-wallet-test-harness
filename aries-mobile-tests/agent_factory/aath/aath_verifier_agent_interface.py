"""
Absctact Base Class for actual issuer agent interfaces to implement
"""

from agent_factory.verifier_agent_interface import VerifierAgentInterface
from agent_factory.aath.aath_agent_interface import AATHAgentInterface
import json
from agent_test_utils import get_qr_code_from_invitation
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected


class AATHVerifierAgentInterface(VerifierAgentInterface, AATHAgentInterface):

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string AATHVerifier"""
        return "AATHVerifier"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False):
        return self.create_invitation_util(oob, print_qrcode, save_qrcode)

    def connected(self):
        return self.connected_util()

    def send_proof_request(self, version=1, request_for_proof=None, connectionless=False):
        """create a proof request """
        
        if connectionless == True:
            topic = "out-of-band"
        else:
            if version == 2:
                topic = "proof-v2"
            else:
                topic = "proof"

        if request_for_proof:
            pass
            # if context.non_revoked_timeframe:
            #     data["non_revoked"] = context.non_revoked_timeframe["non_revoked"]
        else:
            request_for_proof = self.DEFAULT_PROOF_REQUEST.copy()

        presentation_request = {
            "presentation_request": {
                "comment": f"proof request from {self.get_issuer_type()} {self.endpoint}",
                "proof_request": {"data": request_for_proof},
            }
        }

        if connectionless:
            # connectionless proof requests need to call the proof/create-request endpoint first. Then get the id out of it and add it to the data
            # for the out-of-band/create-invitation endpoint.
            (resp_status, resp_text) = agent_controller_POST(
                self.endpoint + "/agent/command/",
                "proof",
                operation="create-request",
                data=presentation_request,
            )
            if resp_status != 200:
                raise Exception(
                    f"Call to create the proof request failed: {resp_status}; {resp_text}"
                )
            else:
                self.create_request_json = json.loads(resp_text)

            presentation_request = {
                "attachments": [self.create_request_json["record"]["presentation_request_dict"]]
            }
            operation = "send-invitation-message"
        else:
            presentation_request["connection_id"] = self.invitation_json['connection_id']
            operation = "send-request"

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/",
            topic,
            operation=operation,
            data=presentation_request,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to send proof request failed: {resp_status}; {resp_text}"
            )
        else:
            self.proof_request_json = json.loads(resp_text)
            if connectionless:
                qrcode = get_qr_code_from_invitation(self.proof_request_json, print_qr_code=False, save_qr_code=True)
                return qrcode


