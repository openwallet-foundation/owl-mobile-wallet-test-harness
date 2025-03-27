from agent_factory.verifier_agent_interface import VerifierAgentInterface
from agent_factory.traction.traction_agent_interface import TractionAgentInterface
import requests

class TractionVerifierAgentInterface(VerifierAgentInterface, TractionAgentInterface):
    
    proof_request_json = {}
    
    def __init__(self, endpoint):
        super().__init__(endpoint)
        print("Traction Verifier init")

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string TractionVerifier"""
        return "TractionVerifier"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40):
        print("CREATE VERIFIER CONNECTION")
        return self.create_invitation_util(oob, print_qrcode, save_qrcode, qr_code_border)

    def connected(self):
        return self.connected_util()

    def send_proof_request(self, version=1, request_for_proof=None, connectionless=False):
        """create a proof request """
        self._fetch_token()
        
        if connectionless:
            raise Exception("Connectionless proof requets are not supported yet")

        if request_for_proof == None:
            request_for_proof = self.DEFAULT_PROOF_REQUEST.copy()

        presentation_request = {
            "connection_id": self._connection_id,
            "auto_verify": False,
            "trace": False,
            "comment": f"proof request from {self.get_issuer_type()} {self.endpoint}",
            "presentation_request": {
                "indy": request_for_proof,
            }
        }

        proof_endpoint = f"{self.endpoint}/present-proof-2.0/send-request"
        proof_sent_response = requests.post(proof_endpoint, json=presentation_request, headers=self._build_headers())

        if proof_sent_response.status_code != 200:
            raise Exception(
                f"Call to send proof request failed: {proof_sent_response.status_code}; {proof_sent_response.text}"
            )
        self.proof_request_json = proof_sent_response.json()

    def proof_request_verified(self):
        """return true if proof request verified"""
        thread_id = self.create_request_json["record"]["thread_id"]
        return expected_agent_proof_state(
            self.endpoint,
            thread_id=thread_id,
            status_txt=["true"],
            wait_time=10.0,
        )