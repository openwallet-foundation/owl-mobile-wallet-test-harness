"""
Class for actual AATH issuer agent
"""

from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_factory.aath.aath_agent_interface import AATHAgentInterface
import json
from agent_test_utils import get_qr_code_from_invitation
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from random import randint

class AATHIssuerAgentInterface(IssuerAgentInterface, AATHAgentInterface):

    _my_public_did: str
    _schema: dict
    _credential_definition: dict
    _credential_json_dict: dict

    def __init__(self, endpoint):
        self._my_public_did = None
        self._schema = None
        self._credential_definition = None
        self._credential_json_dict = {}
        super().__init__(endpoint)

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string AATHIssuer"""
        return "AATHIssuer"

    def create_invitation(self, oob=False, print_qrcode=False, save_qrcode=False):
        return self.create_invitation_util(oob, print_qrcode, save_qrcode)
        

    def connected(self):
        return self.connected_util()


    def send_credential(self, version=1, schema=None, credential_offer=None, revokable=False):
        """send a credential to the holder"""

        if version == 2:
            topic = "issue-credential-v2"
            type = "issue-credential/2.0/credential-preview"
        else:
            topic = "issue-credential"
            type = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview"

        # How is the schema and cred def setup? Should be done here in the agent interface. Need to check if it exists first
        if self._my_public_did is None:
            self._get_public_did()
        if schema is None:
            self._schema = self.DEFAULT_SCHEMA_TEMPLATE.copy()
        else:
            self._schema = schema
        # Check for an existing schema. If it doesn't exist create it.
        if self._schema.get("schema_id") is None:
            self._create_schema(self._schema)
        # Check for an existing credential definition. If it doesn't exist create it.
        if self._credential_definition is None or self._credential_definition.get("credential_definition_id") is None or self._credential_definition.get("schema_id") != self._schema.get("schema_id"):
            if schema is None:
                self._credential_definition = self.DEFAULT_CRED_DEF_TEMPLATE.copy()
            else:
                # self._credential_definition = {
                #     "schema_id": self._schema["schema_id"],
                #     "tag": str(randint(1, 10000)),
                # }
                self._credential_definition = {
                    "schema_id": self._schema["schema_id"],
                    "tag": self._schema["schema_name"],
                }
            self._create_credential_definition(
                self._credential_definition, revokable)

        # if data is none, use a default cred
        # if data is not none then use it as the cred
        if credential_offer:
            cred_data = credential_offer["attributes"] 
        else:
            cred_data = self.DEFAULT_CREDENTIAL_ATTR_TEMPLATE.copy()

        cred_offer = {
            "cred_def_id": self._credential_definition["credential_definition_id"],
            "credential_preview": {
                "@type": type,
                "attributes": cred_data,
            },
            "connection_id": self.invitation_json['connection_id'],
        }

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/",
            topic,
            operation="send-offer",
            data=cred_offer,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to send credential failed: {resp_status}; {resp_text}"
            )
        else:
            self.credential_json = json.loads(resp_text)
            # also add it to the credential json dict just in case we the tests are using multiple credentials
            self._credential_json_dict[self._credential_definition["tag"]] = self.credential_json


    def revoke_credential(self, publish_immediately=True, notify_holder=False, credential=None):
        """revoke a credential"""
        topic = "revocation"

        if credential:
            # get the cred_rev_id and rev_reg_id from the credential given the credential name
            cred_rev_id, rev_reg_id = self._get_revocation_ids(self._credential_json_dict[credential]["thread_id"]);
        else:
            cred_rev_id, rev_reg_id = self._get_revocation_ids(self.credential_json["thread_id"]);

        credential_revocation = {
            "cred_rev_id": cred_rev_id,
            "rev_registry_id": rev_reg_id,
            "publish_immediately": publish_immediately,
        }

        # If Notification is on then add the connection id to the revoke 
        if notify_holder:
            credential_revocation["notify_connection_id"] = self.invitation_json['connection_id']

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/agent/command/",
            topic,
            operation="revoke",
            data=credential_revocation,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to revoke credential failed: {resp_status}; {resp_text}"
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
            self._my_public_did = resp_json["did"]

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

    def _get_revocation_ids(self, thread_id):

        (resp_status, resp_text) = agent_controller_GET(
            self.endpoint + "/agent/response/",
            "revocation-registry",
            id=thread_id,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to get revocation ids failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            cred_rev_id = resp_json["revocation_id"]
            rev_reg_id = resp_json["revoc_reg_id"]
            return cred_rev_id, rev_reg_id