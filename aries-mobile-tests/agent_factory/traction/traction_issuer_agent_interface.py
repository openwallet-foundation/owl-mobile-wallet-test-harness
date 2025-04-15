from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_factory.traction.traction_agent_interface import TractionAgentInterface
from agent_test_utils import get_qr_code_from_invitation
from typing import Optional
import requests
import json
import time


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
        sauce_labs_schema = json.load(open("features/data/schema_sauce_labs_test.json"))

        print("Photo schema")
        self._schema_setup(photo_schema)
        self._schema_setup(drivers_license_1)
        self._schema_setup(drivers_license_2)
        self._schema_setup(photo_revokable)
        self._schema_setup(sauce_labs_schema)
        print("Finished loading schemas")

    def _schema_setup(self, schema):
        schema_id = self._get_schema_id_for_name(schema["schema_name"])
        cred_def_id = self._get_cred_def_id_for_name(schema["schema_name"])

        if schema_id == None:
            new_schema = self._register_schema(schema)
            schema_id = new_schema["sent"]["schema_id"]
        if cred_def_id == None:
            # traction needs time to wrtie schemas to the ledger
            # don't love this but it will only run the first time a test is run with a traction instance
            time.sleep(5)
            new_cred_def =self._register_cred_def(schema_id)
            cred_def_id = new_cred_def['sent']['credential_definition_id']
        
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
        print(f"Register Schema {schema['schema_name']}")
        register_endpoint = f"{self.endpoint}/schemas"
        response = requests.post(
            register_endpoint, headers=self._build_headers(), json=schema
        )
        if response.status_code != 200:
            raise Exception(
                f"Call to register schema failed: {response.text}"
            )
        return response.json()

    def _register_cred_def(self, schema_id, tag="default"):
        print("Register Cred Def")
        register_endpoint = f"{self.endpoint}/credential-definitions"
        response = requests.post(
            register_endpoint,
            headers=self._build_headers(),
            json={
                "revocation_registry_size": 1000,
                "schema_id": schema_id,
                "support_revocation": True,
                "tag": tag,
            },
        )
        if response.status_code != 200:
            raise Exception(
                f"Call to register cred def failed: {response.status_code}: {response.text}"
            )
        return response.json()

    def get_issuer_type(self) -> str:
        """return the type of issuer as a string TractionIssuer"""
        return "TractionIssuer"

    def create_invitation(
        self, oob=False, print_qrcode=False, save_qrcode=False, qr_code_border=40
    ):
        return self.create_invitation_util(oob, print_qrcode, save_qrcode, qr_code_border)

    def connected(self):
        print("Check connection status of issuer")
        return self.connected_util()

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
    def revoke_credential(self, publish_immediately=True, notify_holder=False, credential=None):
        revoke_url = f"{self.endpoint}/revocation/revoke"
        revocation = {
            "cred_ex_id": self.credential_json["cred_ex_id"],
            "publish_immediately": publish_immediately,
        }

        if notify_holder:
            revocation["connection_id"] = self._connection_id

        response = requests.post(revoke_url, json=revocation, headers=self._build_headers())

        if response.status_code != 200:
            raise Exception(
                f"Call to revoke credential failed: {response.status_code}: {response.text}"
            )
        
        # remove old credential refernece
        self.credential_json = {}
        

    def _get_public_did(self):
        did_endpoint = f"{self.endpoint}/wallet/did?method=sov&posture=public"
        wallet_dids = requests.get(did_endpoint).json()
        if len(wallet_dids["results"]) <= 0:
            raise Exception(
                "Public DID not available, traction tenant needs to be an issuer"
            )

        self._my_public_did = wallet_dids["results"][0]["did"]
        return self._my_public_did

    def _get_revocation_ids_for_credential_exchange_id(self, credential_exchange_id):
        # use thread Id to 
        revocation_ids_url = f"{self.endpoint}/revocation/credential-record?cred_ex_id={credential_exchange_id}"
        response = requests.get(revocation_ids_url, headers=self._build_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Call to get revocation ids failed: {response.status_code}: {response.text}"
            )