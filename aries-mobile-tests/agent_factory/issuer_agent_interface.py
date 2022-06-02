"""
Absctact Base Class for actual issuer agent interfaces to implement
"""

from abc import ABC, abstractmethod

class IssuerAgentInterface(ABC):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    # Default schema and cred
    DEFAULT_SCHEMA_TEMPLATE = {
        "schema_name": "test_schema.",
        "schema_version": "1.0.0",
        "attributes": ["attr_1", "attr_2", "attr_3"],
    }

    DEFAULT_CRED_DEF_TEMPLATE = {
        "support_revocation": False,
        "schema_id": "",
        #"tag": str(randint(1, 10000)),
        "tag": "Default AATH Issuer Credential Definition",
    }

    DEFAULT_CREDENTIAL_ATTR_TEMPLATE = [
        {"name": "attr_1", "value": "value_1"},
        {"name": "attr_2", "value": "value_2"},
        {"name": "attr_3", "value": "value_3"},
]

    @abstractmethod
    def get_issuer_type(self) -> str:
        """return the type of issuer you are ie 'AATHIssuer' or 'CANdyWebIssuer'"""

    @abstractmethod
    def create_invitation(self, oob: bool = False, print_qrcode: bool = False, save_qrcode: bool = False):
        """create an invitation and return the json back to the caller """
        # Should we return the actual QR code as an image here? Would make the tests easier

    @abstractmethod
    def connected(self) -> bool:
        """return True/False indicating if this issuer is connected to the wallet holder """

    @abstractmethod
    def send_credential(self, version: int = 1, credential_data=None, revokable: bool = False):
        """create an invitation and return the json back to the caller """

    @abstractmethod
    def revoke_credential(self):
        """revoke a credential"""