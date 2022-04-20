# Externalizing Credential and Proof Test Data<!-- omit in toc -->

## Contents<!-- omit in toc -->

-  [Default Test Credentials](#default-test-credentials)
-  [Defining Tests in Feature Files w/ Externalized Credential Data](#defining-tests-in-feature-files-with-externalized-credential-data)
-  [Defining Tests in Feature Files w/ Externalized Proof Data](#defining-tests-in-feature-files-with-externalized-proof-data)
-  [Summary](#summary)

## Default Test Credentials
Each Issuer and Verifier agent interface implemented in AMTH should have a default credential and a default proof that are created and used when no parameters are are passed to the interface to send a credential offer or send a proof request. This is the case with the current AATH issuer and verfier interfaces. In this case we may have the need to change the type of credential and the type of proof used, to do this we can externalize this test data into json data files. This is what this document will explain.

Other interfaces to other issuers or verfiers may have only one type of credential or proof it uses, so in this case the default is the only one used. You may wish to populate the credential with test data, this is simply accomplished with the normal approach of using data tables in the feature file Scenarios. 

The use of externalized data is illustrated in the BC Wallet tests that are included in the AMTH repo. You can look at these test cases to dig into examples of this externalization of credential and proof test data; `@T002.1-CredentialOffer` `@T002.1-Proof`
 
## Defining Tests in Feature Files with Externalized Credential Data
Tests that have externalized input data for credentials and proofs use Example Data Tables to feed the test with input data. This input data is contained in json files located in `/aries-mobile-test-harness/mobile-test-harness/features/data` for general usage, and in `/aries-mobile-test-harness/mobile-test-harness/features/data/<wallet>` for specific usage. 

```gherkin
   @T002.1-CredentialOffer @critical @AcceptanceTest
   Scenario Outline: Holder accepts the credential offer recieved
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And a connection has been successfully made
      And the user has a credential offer for <credential>
      When they select Accept
      And the holder is informed that their credential is on the way with an indication of loading
      And once the credential arrives they are informed that the Credential is added to your wallet
      And they select Done
      Then they are brought to the list of credentials
      And the credential accepted is at the top of the list
         | issuer_agent_type | credential_name |
         | AATHIssuer        | Photo Id        |

      Examples:
         | credential         |
         | cred_data_photo_id |
```

In the credential offer example above the data for the credential offered is in a json file called `/aries-mobile-test-harness/mobile-test-harness/features/data/cred_data_photo_id.json`. It contains the following;
```json
{
   "schema_name": "photo_id",
   "schema_version": "1.0.0",
   "attributes": [
      {
         "name": "name",
         "value": "Betty Naroff"
      },
      {
         "name": "civic_address",
         "value": "159 Cedar Street, Sudbury, ON"
      },
      ...
      },
      {
         "name": "photo",
         "value": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAWAAAADICAIAAABZO6wsAAAAAXNSR0IArs4c6QAAAARnQ..."
      },
      {
         "name": "issue_date",
         "value": "2022-04-04T13:32:55.455Z"
      },
      {
         "name": "expiry_date",
         "value": "2027-04-04T13:32:55.455Z"
      }
   ]
}
```

These are the attributes and values that will be offered to the holder in this test case. Notice that this data holds a `schema_name` and `schema_version`. These fields are used to get the credential type information from a corrisponding json file called `schema_photo_id.json`. This file is used in the AATH agents to check if the schema exists, create a schema and credential defininition. The contents of this json file are;
```json
{
   "schema_name":"photo_id",
   "schema_version":"1.0.0",
   "attributes":[
      "name",
      "civic_address",
      "city",
      "province",
      "country",
      "postal_code",
      "birth_dateint",
      "photo",
      "issue_date",
      "expiry_date"
   ]
}
```
Follow these patterns and json file structure/schema to create your own credetials to use with AATH issuer and verifier agents or your own agents. 


## Defining Tests in Feature Files with Externalized Proof Data
Proof Requests case follow the same pattern as the Credential Offer case above. This proof request data file is a proof request for the credential above.

```gherkin
   @T002.1-Proof @critical @AcceptanceTest
   Scenario Outline: Holder accepts the proof request
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name |
         | AATHIssuer        | Photo Id        |
      And the user has a proof request for <proof>
      When they select Share
      And the holder is informed that they are sending information securely
      And once the proof is verified they are informed of such
      And they select Done on the verfified information
      Then they are brought Home

      Examples:
         | credential         | proof          |
         | cred_data_photo_id | proof_photo_id |
```
The addition of the proof in this sceanrio adds a `proof_photo_id` in the table data that corrisponds to the `/aries-mobile-test-harness/mobile-test-harness/features/data/proof_photo_id.json`. It contains the contexts of the proof request that gets passed to the AATH Verifier Agent.
```json
{
   "requested_attributes": {
      "photo_attrs": {
         "names": [
               "photo"
            ],
         "restrictions": [
               {
                  "schema_name": "photo_id",
                  "schema_version": "1.0.0"
               }
         ]
      }
   },
   "requested_predicates": {
      "age": {
         "name": "birth_dateint",
         "p_type": ">",
         "p_value": 19420116,
         "restrictions": [
               {
                  "schema_name": "photo_id",
                  "schema_version": "1.0.0"
               }
         ]
      }
   },
   "version": "0.1.0"
}
```

## Summary
With the constructs above is should be very easy to add new tests based off of new credentials and proofs, along with running existing tests with new credentials and proofs. Essentially, once the json files are created, opening a credential offer or proof feature file, adding a row to the examples data table, one should have a new running test scenario with those new credentials.

Keep in mind that this currently works with the AATH issuer and verifier agents. As we move forward these same data files could be used with other issuers or verifiers, but it is likely that those agents will have thier own inbred credentials and proofs. Alternate forms of test data marshalling may need to be considered with other agents.