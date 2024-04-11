"""
Absctact Base Class for actual issuer agent interfaces to implement
"""

import json

from agent_controller_client import (agent_controller_GET,
                                     agent_controller_POST,
                                     expected_agent_proof_state,
                                     expected_agent_state,
                                     setup_already_connected)
from agent_factory.aath.aath_agent_interface import AATHAgentInterface
from agent_factory.verifier_agent_interface import VerifierAgentInterface
from agent_test_utils import get_qr_code_from_invitation


class MCNVerifierAgentInterface(VerifierAgentInterface, AATHAgentInterface):
    """MCN Verifier for Acapy Version 0.9.0"""

    DEFAULT_PROOF_REQUEST = {
        "requested_attributes": {
            "attr_1": {
                "name": "attr_1",
                "restrictions": [
                    {
                        "schema_name": "test_schema",
                        "schema_version": "1.0.0",
                    }
                ],
            }
        },
        "requested_predicates": {},
    }

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string MCNVerifier"""
        return "MCNVerifier"

    def connected_util(self) -> bool:
        """return True/False indicating if this issuer is connected to the wallet holder"""

        # If OOB then make a call to get the connection id from the webhook.
        if self._oob == True:
            # Get the responders's connection id from the above request's response webhook in the backchannel
            invitation_id = self.invitation_json["invitation"]["@id"]
            (resp_status, resp_text) = agent_controller_GET(
                self.endpoint + "/", f"connections?invitation_msg_id={invitation_id}"
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
            connection_id = self.invitation_json["connection_id"]
        return expected_agent_state(
            self.endpoint + "/",
            "connections",
            connection_id,
            "completed",
            sleep_time=2.0,
        )

    def create_invitation_util(
        self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40
    ):
        """create an invitation and return the json back to the caller"""
        self._oob = oob
        if self._oob is True:
            data = {
                "use_public_did": False,
                "handshake_protocols": ["https://didcomm.org/connections/1.0"],
            }
            (resp_status, resp_text) = agent_controller_POST(
                self.endpoint + "/",
                "out-of-band",
                operation="create-invitation",
                data=data,
            )
        else:
            (resp_status, resp_text) = agent_controller_POST(
                self.endpoint + "/",
                "connections",
                operation="create-invitation",
            )

        if resp_status != 200:
            raise Exception(
                f"Call to create connection invitation failed: {resp_status}; {resp_text}"
            )
        else:
            self.invitation_json = json.loads(resp_text)
            if "label" in self.invitation_json["invitation"]:
                self.name = self.invitation_json["invitation"]["label"]
            qrimage = get_qr_code_from_invitation(
                self.invitation_json, print_qrcode, save_qrcode, qr_code_border
            )
            return qrimage

    def create_invitation(
        self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40
    ):
        return self.create_invitation_util(
            oob, print_qrcode, save_qrcode, qr_code_border
        )

    def connected(self):
        return self.connected_util()

    def send_proof_request(
        self, version=1, request_for_proof=None, connectionless=False
    ):
        """create a proof request"""

        if connectionless == True:
            topic = "out-of-band"
        else:
            if version == 2:
                topic = "present-proof-2.0"
            else:
                topic = "present-proof"

        if request_for_proof:
            pass
            # if context.non_revoked_timeframe:
            #     data["non_revoked"] = context.non_revoked_timeframe["non_revoked"]
        else:
            request_for_proof = self.DEFAULT_PROOF_REQUEST.copy()

        presentation_request = {
            "comment": f"proof request from {self.get_issuer_type()} {self.endpoint}",
            "proof_request": request_for_proof,
        }

        if connectionless:
            # connectionless proof requests need to call the proof/create-request endpoint first. Then get the id out of it and add it to the data
            # for the out-of-band/create-invitation endpoint.
            (resp_status, resp_text) = agent_controller_POST(
                self.endpoint + "/",
                "present-proof",
                operation="create-request",
                data=presentation_request,
                wrap_data_with_data=False,
            )
            if resp_status != 200:
                raise Exception(
                    f"Call to create the proof request failed: {resp_status}; {resp_text}"
                )
            else:
                self.create_request_json = json.loads(resp_text)

            presentation_request = {
                "attachments": [self.create_request_json["presentation_request_dict"]]
            }
            operation = "create-invitation"
        else:
            presentation_request["connection_id"] = self.invitation_json[
                "connection_id"
            ]
            operation = "send-request"

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/",
            topic,
            operation=operation,
            data=presentation_request,
            wrap_data_with_data=False,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to send proof request failed: {resp_status}; {resp_text}"
            )
        else:
            print(f"Status Code: {resp_status}, REQUESTED PROOF")
            self.proof_request_json = json.loads(resp_text)
            if connectionless:
                qrcode = get_qr_code_from_invitation(
                    self.proof_request_json, print_qr_code=False, save_qr_code=True
                )
                return qrcode

    def proof_request_verified(self):
        """return true if proof request verified"""
        thread_id = self.create_request_json["record"]["thread_id"]
        return expected_agent_proof_state(
            self.endpoint,
            thread_id=thread_id,
            status_txt=["true"],
            wait_time=10.0,
        )
