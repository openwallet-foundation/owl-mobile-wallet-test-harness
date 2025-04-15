"""
Absctact Base Class for actual verifier agent interfaces to implement
"""

from abc import ABC, abstractmethod


class VerifierAgentInterface(ABC):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    # Default schema and cred
    DEFAULT_PROOF_REQUEST = {
        "name": "Sauce labs default proof request",
        "nonce": "1234567890",
        "version": "1.0",
        "requested_attributes": {
            "attr_1": {
                "names": ["first_name"],
                "restrictions": [
                    {
                        "schema_name": "sauce_labs_test"
                    }
                ],
            }
        },
        "requested_predicates": {}
    }

    @abstractmethod
    def get_issuer_type(self) -> str:
        """return the type of issuer you are ie 'AATHVerifier'"""

    @abstractmethod
    def send_proof_request(self):
        """do a proof request"""
