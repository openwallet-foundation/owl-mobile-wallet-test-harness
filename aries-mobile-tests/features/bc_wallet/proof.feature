# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/29
@Proof @bc_wallet @Story_29
Feature: Proof
   In order to easily prove my credential details to a verifier
   As a holder
   I want to be able to review, accept, and decline a proof request


   @T001-Proof @critical @AcceptanceTest @Story_29
   Scenario: Holder receives and views the contents of a proof request
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And a connection has been successfully made
      And the holder has a Non-Revocable credential
         | issuer_agent_type | credential_name |
         | AATHIssuer        | Test Schema     |
      When the Holder scans the QR code sent by the "verifier"
      And the Holder is taken to the Connecting Screen/modal
      And the Connecting completes successfully
      And the Holder receives a proof request
      Then holder is brought to the proof request
      And they can view the contents of the proof request
         | verifier_agent_type | who        | attributes | values  |
         | AATHVerifier        | aca-py.Bob | Attr 1     | value_1 |
   #| CANdyWebIssuer    | # CANdy - Unverified Person Issuer | Unverified Person | First Name;Last Name;Date of Birth;Street Address;Postal Code;City;Province;Country;Issued | Sheldon;Regular;1989-03-04;123 Perfect Street;A2V 3E1;Awesome City;BC;Canada;2022-03-14T23:27:20.133Z |


   @T002-Proof @critical @AcceptanceTest @Story_29 @SmokeTest
   Scenario: Holder accepts the proof request
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And a connection has been successfully made
      And the holder has a Non-Revocable credential
         | issuer_agent_type | credential_name |
         | AATHIssuer        | Test Schema     |
      And the user has a proof request
      When they select Share
      And the holder is informed that they are sending information securely
      And once the proof is verified they are informed of such
      And they select Done on the verfified information
      Then they are brought Home


   @T002.1-Proof @critical @AcceptanceTest @Story_29
   Scenario Outline: Holder accepts the proof request
      Given the User has skipped on-boarding
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


   @T003-Proof @critical @AcceptanceTest @Revocation
   Scenario Outline: Holder accepts the proof request of a revoked credential where the verifier cares if the credential was revoked
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name    |
         | AATHIssuer        | Photo Id Revokable |
      And the credential has been revoked by the issuer
      When the user has a proof request for <proof> including proof of non-revocation at <interval>
      Then they can only select Decline
      And they are asked if they are sure they want to decline the Proof
      And they Confirm the decline
      And they are brought home

      Examples:
         | credential                   | proof                    | interval |
         | cred_data_photo_id_revokable | proof_photo_id_revokable | now:now  |


   @T004-Proof @critical @AcceptanceTest @Revocation @wip
   Scenario Outline: Holder accepts the proof request of a non-revoked revokable credential where the verifier cares if the credential was revoked



   @T005-Proof @critical @AcceptanceTest @Revocation @wip
   Scenario Outline: Holder accepts the proof request of a revoked credential where the verifier doesn't care if the credential was revoked



   @T006-Proof @critical @AcceptanceTest @Revocation @wip
   Scenario Outline: Holder accepts the proof request of a non-revoked revokable credential where the verifier doesn't care if the credential was revoked


   @T007-Proof @critical @AcceptanceTest @Revocation @wip
   Scenario Outline: Holder accepts the proof request of a non-revoked credential and presents a non-revokable credential
# if a non-revokable credential can be presented then that should take precedent over revokable credentials since it de facto satisfies proof of non-revocation.

#Connectionless