from agent_factory.verifier_agent_interface import VerifierAgentInterface
from agent_factory.traction.traction_agent_interface import TractionAgentInterface
from agent_test_utils import get_qr_code_from_invitation
import requests
import json

class TractionVerifierAgentInterface(VerifierAgentInterface, TractionAgentInterface):
    
    proof_request_json = {}
    
    def __init__(self, endpoint):
        super().__init__(endpoint)
        print("Traction Verifier init")

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string TractionVerifier"""
        return "TractionVerifier"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40):
        print("CREATE AN INVITATION...")
        return self.create_invitation_util(oob, print_qrcode, save_qrcode, qr_code_border)

    def connected(self):
        return True
        # return self.connected_util()


    def send_proof_request_1(self, version=1, request_for_proof=None, connectionless=False):

        pass
    def send_proof_request(self, version=1, request_for_proof=None, connectionless=False):
        """create a proof request """
        
        if connectionless:
            raise Exception("Connectionless proof requets are not supported yet")

        if request_for_proof == None:
            request_for_proof = self.DEFAULT_PROOF_REQUEST.copy()

        presentation_request = {
            "presentation_request": {
                "comment": f"proof request from {self.get_issuer_type()} {self.endpoint}",
                "proof_request": {"data": request_for_proof},
            }, 
            "connection_id": self.invitation_json["connection_id"]
        }

        print(presentation_request)

        # make request to traction
        proof_endpoint = f"{self.endpoint}/present-proof-2.0/send-request"
        (resp_status, resp_text) = requests.post(proof_endpoint, headers=self._build_headers(), data=presentation_request)

        if resp_status != 200:
            raise Exception(
                f"Call to send proof request failed: {resp_status}; {resp_text}"
            )
        self.proof_request_json = json.loads(resp_text)

    def proof_request_verified(self):
        """return true if proof request verified"""
        thread_id = self.create_request_json["record"]["thread_id"]
        return expected_agent_proof_state(
            self.endpoint,
            thread_id=thread_id,
            status_txt=["true"],
            wait_time=10.0,
        )