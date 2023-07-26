"""
Absctact Base Class for actual verifier agent interfaces to implement
"""

from abc import ABC, abstractmethod


class VerifierAgentInterface(ABC):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    # Default schema and cred
    DEFAULT_PROOF_REQUEST = {
        "requested_attributes": {
            "attr_1": {
                "name": "attr_1",
                "restrictions": [
                    {
                        "schema_name": "test_schema.",
                        "schema_version": "1.0.0",
                    }
                ],
            }
        }
    }

    @abstractmethod
    def get_issuer_type(self) -> str:
        """return the type of issuer you are ie 'AATHVerifier'"""

    @abstractmethod
    def send_proof_request(self):
        """do a proof request"""
