"""
Absctact Base Class for actual issuer agent interfaces to implement
"""

from agent_factory.issuer_agent_interface import IssuerAgentInterface
import json
from agent_test_utils import get_qr_code_from_invitation
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected


class AATHIssuerAgentInterface(IssuerAgentInterface):

    _my_public_did: str
    _schema: dict
    _credential_definition: dict

    def __init__(self, endpoint):
        self._my_public_did = None
        self._schema = None
        self._credential_definition = None
        super().__init__(endpoint)

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string AATHIssuer"""
        return "AATHIssuer"

    def create_invitation(self, oob=False):
        """create an invitation and return the json back to the caller """
        self.oob = oob
        if self.oob is True:
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
            qrimage = get_qr_code_from_invitation(self.invitation_json)
            return qrimage

    def connected(self):
        """return True/False indicating if this issuer is connected to the wallet holder """

        # If OOB then make a call to get the connection id from the webhook. 
        if self.oob == True:
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
        else:
            connection_id = self.invitation_json['connection_id']
        return expected_agent_state(self.endpoint, "connection", connection_id, "complete", sleep_time=2.0)

    def send_credential(self, version=1, schema=None, credential_offer=None, revokable=False):
        """send a credential to the holder"""

        # How is the schema and cred def setup? Should be done here in the agent interface. Need to check if it exists first
        if self._my_public_did is None:
            self._get_public_did()
        if schema is None:
            self._schema = self.DEFAULT_SCHEMA_TEMPLATE.copy()
        else:
            # TODO may have to pass a schema in from the tests.
            self._schema = schema
        # Check for an existing schema. If it doesn't exist create it.
        if self._schema.get("schema_id") is None:
            self._create_schema(self._schema)
        # Check for an existing credential definition. If it doesn't exist create it.
        if self._credential_definition is None or self._credential_definition.get("credential_definition_id") is None:
            self._credential_definition = self.DEFAULT_CRED_DEF_TEMPLATE.copy()
            self._create_credential_definition(
                self._credential_definition, revokable)

        # Where to get the credential data?
        # if data is none, use a default cred
        # if data is not none then use it as the cred
        cred_data = credential_offer or self.DEFAULT_CREDENTIAL_ATTR_TEMPLATE.copy()

        cred_offer = {
            "cred_def_id": self._credential_definition["credential_definition_id"],
            "credential_preview": {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
                "attributes": cred_data,
            },
            "connection_id": self.invitation_json['connection_id'],
        }

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/",
            "issue-credential",
            operation="send-offer",
            data=cred_offer,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to send credential failed: {resp_status}; {resp_text}"
            )
        else:
            self.credential_json = json.loads(resp_text)

    def _get_public_did(self):
        (resp_status, resp_text) = agent_controller_GET(
            self.endpoint + "/agent/command/", "did"
        )
        if resp_status != 200:
            raise Exception(
                f"Call to get issuer public did failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            self.__my_public_did = resp_json["did"]

    def _create_schema(self, schema):
        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/", "schema", data=schema
        )
        if resp_status != 200:
            raise Exception(
                f"Call to create schema failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            self._schema["schema_id"] = resp_json["schema_id"]

    def _create_credential_definition(self, cred_def, revokable):
        cred_def["schema_id"] = self._schema["schema_id"]

        if revokable:
            cred_def["support_revocation"] = True

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/", "credential-definition", data=cred_def
        )
        if resp_status != 200:
            raise Exception(
                f"Call to create credential definition failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            self._credential_definition["credential_definition_id"] = resp_json["credential_definition_id"]
