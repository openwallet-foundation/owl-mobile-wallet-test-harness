from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_factory.traction.traction_agent_interface import TractionAgentInterface
from agent_test_utils import get_qr_code_from_invitation
from typing import Optional
import requests
import json


class TractionIssuerAgentInterface(TractionAgentInterface, IssuerAgentInterface):

    _schemas: dict
    _credential_definitions: dict
    _credential_json_dict: dict

    def __init__(self, endpoint):
        super().__init__(endpoint)
        self._load_schemas()

    def _load_schemas(self):
        print("Load schemas")
        photo_schema = json.load(open("features/data/schema_photo_id.json"))
        drivers_license_1 = json.load(
            open("features/data/schema_drivers_license_😀.json")
        )
        drivers_license_2 = json.load(open("features/data/schema_drivers_license.json"))
        photo_revokable = json.load(
            open("features/data/schema_photo_id_revokable.json")
        )

        self._schema_setup(photo_schema)
        self._schema_setup(drivers_license_1)
        self._schema_setup(drivers_license_2)
        self._schema_setup(photo_revokable)
        self._schema_setup(
            {
                "schema_name": "sauce_labs_test",
                "schema_version": "1.0",
                "attributes": ["first_name", "last_name"],
            }
        )
        print("Finished loading schemas")

    def _schema_setup(self, schema):
        schema_id = self._get_schema_id_for_name(schema["schema_name"])
        cred_def_id = self._get_cred_def_id_for_name(schema["schema_name"])

        if schema_id == None:
            new_schema = self._register_schema(schema)
            schema_id = new_schema["sent"]["schema"]["id"]

        if cred_def_id == None:
            cred_def_id = self._register_cred_def(schema_id)

        self._schemas[schema["schema_name"]] = self._get_schema_for_id(schema_id)[
            "schema"
        ]
        self._credential_definitions[schema["schema_name"]] = self._get_cred_def_for_id(
            cred_def_id
        )["credential_definition"]
        print("Setup for schema: ", schema["schema_name"], " is done!")

    def _get_schema_for_id(self, id) -> dict:
        schema_endpoint = f"{self.endpoint}/schemas/{id}"
        return requests.get(schema_endpoint, headers=self._build_headers()).json()

    def _get_cred_def_for_id(self, id) -> dict:
        cred_def_endpoint = f"{self.endpoint}/credential-definitions/{id}"
        return requests.get(cred_def_endpoint, headers=self._build_headers()).json()

    def _get_schema_id_for_name(self, name) -> Optional[str]:
        schema_endpoint = f"{self.endpoint}/schemas/created?schema_name={name}"
        schema_ids = requests.get(schema_endpoint, headers=self._build_headers()).json()
        return (
            schema_ids["schema_ids"][0] if len(schema_ids["schema_ids"]) > 0 else None
        )

    def _get_cred_def_id_for_name(self, name) -> Optional[str]:
        cred_def_endpoint = (
            f"{self.endpoint}/credential-definitions/created?schema_name={name}"
        )
        cred_def_ids = requests.get(
            cred_def_endpoint, headers=self._build_headers()
        ).json()
        return (
            cred_def_ids["credential_definition_ids"][0]
            if len(cred_def_ids["credential_definition_ids"]) > 0
            else None
        )

    def _register_schema(self, schema) -> dict:
        print("Register Schema")
        register_endpoint = f"{self.endpoint}/schemas"
        return requests.post(
            register_endpoint, headers=self._build_headers(), json=schema
        ).json()

    def _register_cred_def(self, schema_id, tag="default"):
        print("Register Cred Def")
        register_endpoint = f"{self.endpoint}/credential-definitions"
        return requests.post(
            register_endpoint,
            headers=self._build_headers(),
            json={
                "revocation_registry_size": 1000,
                "schema_id": schema_id,
                "support_revocation": True,
                "tag": tag,
            },
        ).json()

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string TractionIssuer"""
        return "TractionIssuer"

    def create_invitation(
        self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40
    ):
        return self.create_invitation_util(oob, print_qrcode, save_qrcode, qr_code_border)

    def connected(self):
        print("Check connection status")
        connection_id = ""
        if self._oob == True:
            print("OOB CONNECTION")
            # fetch connection ID from connections
            invite_id = self.invitation_json["invi_msg_id"]
            connection_fetch_rule = f"{self.endpoint}/connections?invitation_msg_id={invite_id}&limit=100&offset=0"
            connection_response = requests.get(
                connection_fetch_rule, headers=self._build_headers()
            )
            results = connection_response.json()
            if results["results"]:
                connection_id = results["results"][0]["connection_id"]
            else:
                raise Exception("OOB Connection record is not found")

        else:
            connection_id = self.invitation_json["connection_id"]
        self._connection_id = connection_id
        connection_ping_url = f"{self.endpoint}/connections/{connection_id}/send-ping"
        ping_response = requests.post(
            connection_ping_url, json={}, headers=self._build_headers()
        )
        return ping_response.status_code == 200

    def revoke_credential(self):
        pass

    def send_credential(
        self, version=2, schema=None, credential_offer=None, revokable=False
    ):
        print("Traction: send credential")
        issue_credential_url = f"{self.endpoint}/issue-credential-2.0/send"

        if credential_offer:
            cred_data = credential_offer["attributes"]
            schema_name = credential_offer["schema_name"]
        else:
            schema_name = "sauce_labs_test"
            cred_data = [
                {"name": "first_name", "value": "Sauce"},
                {"name": "last_name", "value": "Test"},
            ]
        payload = {
            "auto_remove": True,
            "comment": "string",
            "connection_id": self._connection_id,
            "credential_preview": {
                "@type": "issue-credential/2.0/credential-preview",
                "attributes": cred_data,
            },
            "filter": {
                "indy": {"cred_def_id": self._credential_definitions[schema_name]["id"]}
            },
            "trace": True,
            "verification_method": "string",
        }

        response = requests.post(
            issue_credential_url, json=payload, headers=self._build_headers()
        )
        json_response = response.json()
        if response.status_code == 200:
            self.credential_json = json_response
            self._credential_json_dict[schema_name] = json_response
        else:
            raise Exception(
                f"There was an error sending credential to: {self._connection_id}"
            )

    def _get_public_did(self):
        did_endpoint = f"{self.endpoint}/wallet/did?method=sov&posture=public"
        wallet_dids = requests.get(did_endpoint).json()
        if len(wallet_dids["results"]) <= 0:
            raise Exception(
                "Public DID not available, traction tenant needs to be an issuer"
            )

        self._my_public_did = wallet_dids["results"][0]["did"]
        return self._my_public_did
