"""
Base Class for actual AATH agents
"""

import json
from time import sleep
from typing import Union

from agent_controller_client import (agent_controller_GET,
                                     agent_controller_POST,
                                     expected_agent_state,
                                     setup_already_connected)
from agent_factory.aath.aath_agent_interface import AATHAgentInterface
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_test_utils import get_qr_code_from_invitation


class MCNIssuerAgentInterface(IssuerAgentInterface, AATHAgentInterface):
    _my_public_did: Union[str, None]
    _schema: Union[dict, None]
    _credential_definition: Union[dict, None]
    _credential_json_dict: Union[dict, None]

    DEFAULT_SCHEMA_TEMPLATE = {
        "schema_name": "test_schema",
        "schema_id": "Ep31SvFAetugFPe5CGzJxt:2:test_schema:1.0.0",
        "schema_version": "1.0.0",
        "attributes": ["attr_1", "attr_2", "attr_3"],
    }

    DEFAULT_CRED_DEF_TEMPLATE = {
        "support_revocation": False,
        "schema_id": "Ep31SvFAetugFPe5CGzJxt:2:test_schema:1.0.0",
        "tag": "test_schema",
    }

    DEFAULT_CRED_DEF_ID = "Ep31SvFAetugFPe5CGzJxt:3:CL:33888:test_schema"

    def __init__(self, endpoint):
        self._my_public_did = None
        self._schema = None
        self._credential_definition = None
        self._credential_json_dict = {}
        super().__init__(endpoint)

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string MCNIssuer"""
        return "MCNIssuer"

    def create_invitation(
        self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40
    ):
        return self.create_invitation_util(
            oob, print_qrcode, save_qrcode, qr_code_border
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

    def connected(self) -> bool:
        return self.connected_util()

    def revoke_credential(
        self, publish_immediately=True, notify_holder=False, credential=None
    ):
        """revoke a credential"""
        topic = "revocation"

        if credential:
            # get the cred_rev_id and rev_reg_id from the credential given the credential name
            cred_rev_id, rev_reg_id = self._get_revocation_ids(
                self._credential_json_dict[credential]["thread_id"]
            )
        else:
            cred_rev_id, rev_reg_id = self._get_revocation_ids(
                self.credential_json["thread_id"]
            )

        credential_revocation = {
            "cred_rev_id": cred_rev_id,
            "rev_registry_id": rev_reg_id,
            "publish_immediately": publish_immediately,
        }

        # If Notification is on then add the connection id to the revoke
        if notify_holder:
            credential_revocation["notify_connection_id"] = self.invitation_json[
                "connection_id"
            ]

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/",
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
            self.endpoint + "/wallet/", "did/public"
        )
        if resp_status != 200:
            raise Exception(
                f"Call to get issuer public did failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            self._my_public_did = resp_json["result"]["did"]

    def _create_schema(self, schema):
        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/", "schemas", data=schema
        )
        if resp_status != 200:
            raise Exception(f"Call to create schema failed: {resp_status}; {resp_text}")
        else:
            resp_json = json.loads(resp_text)
            self._schema["schema_id"] = resp_json["sent"]["schema"]["id"]

    def _create_credential_definition(self, cred_def, revokable):
        cred_def["schema_id"] = self._schema["schema_id"]

        if revokable:
            cred_def["support_revocation"] = True

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/", "credential-definitions", data=cred_def
        )
        if resp_status != 200:
            raise Exception(
                f"Call to create credential definition failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            self._credential_definition["credential_definition_id"] = resp_json["sent"][
                "credential_definition_id"
            ]

    def _get_revocation_ids(self, thread_id):
        (resp_status, resp_text) = agent_controller_GET(
            self.endpoint + "/",
            "revocation/registry",
            id=thread_id,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to get revocation ids failed: {resp_status}; {resp_text}"
            )
        else:
            resp_json = json.loads(resp_text)
            cred_rev_id = resp_json["cred_def_id"]
            rev_reg_id = resp_json["result"]["revoc_reg_id"]
            return cred_rev_id, rev_reg_id

    def send_credential(
        self, version=1, schema=None, credential_offer=None, revokable=False
    ):
        """send a credential to the holder"""

        if version == 2:
            topic = "issue-credential-2.0"
            type = "issue-credential/2.0/credential-preview"
        else:
            topic = "issue-credential"
            type = "issue-credential/1.0/credential-preview"

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

        if self._credential_definition is None:
            self._credential_definition = self.DEFAULT_CRED_DEF_TEMPLATE.copy()

        self._credential_definition[
            "credential_definition_id"
        ] = self.DEFAULT_CRED_DEF_ID

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
            "connection_id": self.invitation_json["connection_id"],
        }

        (resp_status, resp_text) = agent_controller_POST(
            self.endpoint + "/",
            topic,
            operation="send-offer",
            data=cred_offer,
            wrap_data_with_data=False,
        )
        if resp_status != 200:
            raise Exception(
                f"Call to send credential failed: {resp_status}; {resp_text}"
            )
        else:
            print("ISSUED TEST SCHEMA ATTESTATION")
            self.credential_json = json.loads(resp_text)
            # also add it to the credential json dict just in case we the tests are using multiple credentials
            if self._credential_json_dict is not None:
                self._credential_json_dict[
                    self._credential_definition["tag"]
                ] = self.credential_json
