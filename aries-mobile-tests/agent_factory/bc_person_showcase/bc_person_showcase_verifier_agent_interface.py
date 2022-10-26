"""
Absctact Base Class for actual verifier agent interfaces to implement
"""

from asyncio import sleep
from agent_factory.verifier_agent_interface import VerifierAgentInterface
import json
from agent_test_utils import get_qr_code_from_invitation
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected


class BCPersonShowcaseVerifierAgentInterface(VerifierAgentInterface):

    # Default schema and cred
    DEFAULT_PROOF_REQUEST = {
        "requested_attributes": {
            "Person":{
                "restrictions":[
                    {
                        "schema_name":"Person"
                    }
                ],
                "names":[
                    "picture",
                    "family_name",
                    "given_names",
                    "locality",
                    "region",
                    "postal_code",
                    "street_address",
                    "country",
                    "expiry_date_dateint",
                    "birthdate_dateint"
                ]
            }
        },
        "requested_predicates":{
         
        },
        "version":"1.0.0",
        "name":"BC Digital ID Request"
    }

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string BCPersonShowcaseVerifier"""
        return "BCPersonShowcaseVerifier"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False):
        """create an invitation and return the json back to the caller """
        # https://bc-wallet-demo-agent-admin-test.apps.silver.devops.gov.bc.ca/connections/create-invitation

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
                self.endpoint, topic="/connections", operation="create-invitation"
            )

        if resp_status != 200:
            raise Exception(
                f"Call to create connection invitation failed: {resp_status}; {resp_text}"
            )
        else:
            self.invitation_json = json.loads(resp_text)
            qrimage = get_qr_code_from_invitation(self.invitation_json, print_qrcode, save_qrcode)
            return qrimage

    def connected(self):
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
            connection_id = self.invitation_json['connection']['id']
        
        return self._expected_connection_state(self.endpoint, "/connections", connection_id, "complete", 6, 2)


    def _expected_connection_state(self, agent_url, protocol_txt, id, status_txt, wait_time=2.0, sleep_time=0.5):
        sleep(sleep_time)
        state = "None"
        if type(status_txt) != list:
            status_txt = [status_txt]
        # "N/A" means that the controller can't determine the state - we'll treat this as a successful response
        status_txt.append("N/A")
        #for i in range(int(wait_time/sleep_time)):
        for i in range(int(wait_time)):
            (resp_status, resp_text) = agent_controller_GET(agent_url, protocol_txt, id=id)
            if resp_status == 200:
                resp_json = json.loads(resp_text)
                state = resp_json["state"]
                if state in status_txt:
                    return True
            sleep(sleep_time)

        print("From", agent_url, "Expected state", status_txt, "but received", state, ", with a response status of", resp_status)
        return False

    def send_proof_request(self, version=1, request_for_proof=None, connectionless=False):
        """create a proof request """
        
        if version == 2:
            topic = "proof-v2"
        else:
            topic = "/proofs"

        if request_for_proof:
            pass
            # if context.non_revoked_timeframe:
            #     data["non_revoked"] = context.non_revoked_timeframe["non_revoked"]
        else:
            request_for_proof = self.DEFAULT_PROOF_REQUEST.copy()

        presentation_request = {
            "connectionId": self.invitation_json['connection']['id'],
            "proofRequest": request_for_proof,
            "comment": f"proof request from {self.get_issuer_type()} {self.endpoint}"
        }

        if connectionless:
            operation = "create-send-connectionless-request"
        else:
            #presentation_request["connectionId"] = self.invitation_json['connection']['id']
            operation = "request-proof"

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint,
            topic,
            operation=operation,
            data=presentation_request,
            wrap_data_with_data=False
        )
        if resp_status != 200:
            raise Exception(
                f"Call to send proof request failed: {resp_status}; {resp_text}"
            )
        else:
            self.proof_request_json = json.loads(resp_text)


