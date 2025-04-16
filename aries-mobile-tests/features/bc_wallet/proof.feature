# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/29
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/614
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/63
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
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a Non-Revocable credential
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Sauce Labs Test |
      When the Holder scans the QR code sent by the "verifier"
      And the Holder is taken to the Connecting Screen/modal
      And the Connecting completes successfully
      And the Holder receives a proof request
      And the holder opens the proof request
      Then holder is brought to the proof request
      And they can view the contents of the proof request
         | verifier_agent_type | who                     | attributes | values  |
         | TractionVerifier    | Sauce labs connection   | First Name | Sauce   |
   #| CANdyWebIssuer    | # CANdy - Unverified Person Issuer | Unverified Person | First Name;Last Name;Date of Birth;Street Address;Postal Code;City;Province;Country;Issued | Sheldon;Regular;1989-03-04;123 Perfect Street;A2V 3E1;Awesome City;BC;Canada;2022-03-14T23:27:20.133Z |


   @T002-Proof @critical @AcceptanceTest @Story_29 @SmokeTest
   Scenario: Holder accepts the proof request
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a Non-Revocable credential
         | issuer_agent_type | credential_name                           |
         | TractionIssuer    | Sauce Labs Test |
      And the user has a proof request
      When they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      #And once the proof is verified they are informed of such
      And they select Go back to home on information sent successfully
      #And they select Done on the verfified information
      Then they are brought Home


   @T002.1-Proof @critical @AcceptanceTest @Story_29
   Scenario Outline: Holder accepts the proof request
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Photo Id        |
      And the user has a proof request for <proof>
      When they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      #And once the proof is verified they are informed of such
      And they select Go back to home on information sent successfully
      #And they select Done on the verfified information
      Then they are brought Home

      Examples:
         | credential         | proof          |
         | cred_data_photo_id | proof_photo_id |


   @T002.2-Proof @normal @FunctionalTest @Story_29
   Scenario Outline: Holder accepts the proof request credential has special characters
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And the holder has credentials
         | credential                        | revocable | issuer_agent_type | credential_name    |
         | cred_data_drivers_license_sp_char | True      | TractionIssuer    | Credential         |
      And the user has a proof request for <proof>
      When they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      And they select Go back to home on information sent successfully
      Then they are brought Home

      Examples:
         | proof                         |
         | proof_drivers_license_sp_char |


   @T003-Proof @critical @AcceptanceTest @Revocation
   Scenario Outline: Holder accepts the proof request of a revoked credential where the verifier cares if the credential was revoked
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |
      And the credential has been revoked by the issuer
      When the user has a proof request for <proof> including proof of non-revocation at <interval>
      Then they can only select Decline
      And they are asked if they are sure they want to decline the Proof
      And they Confirm the decline
      And they are brought home

      Examples:
         | credential                   | proof                    | interval |
         | cred_data_photo_id_revokable | proof_photo_id_revokable | now:now  |


   @T004-Proof @normal @AcceptanceTest @Revocation
   Scenario Outline: Holder accepts the proof request of a non-revoked revokable credential where the verifier cares if the credential was revoked
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |
      When the user has a proof request for <proof> including proof of non-revocation at <interval>
      And they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      And they select Go back to home on information sent successfully
      #And once the proof is verified they are informed of such
      #And they select Done on the verfified information
      Then they are brought Home

      Examples:
         | credential                   | proof                    | interval |
         | cred_data_photo_id_revokable | proof_photo_id_revokable | now:now  |


   @T005-Proof @normal @AcceptanceTest @Revocation
   Scenario Outline: Holder accepts the proof request of a revoked credential where the verifier doesn't care if the credential was revoked
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |
      And the credential has been revoked by the issuer
      When the user has a proof request for <proof>
      And they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      And they select Go back to home on information sent successfully
      #And once the proof is verified they are informed of such
      #And they select Done on the verfified information
      Then they are brought Home

      Examples:
         | credential                   | proof                    |
         | cred_data_photo_id_revokable | proof_photo_id_revokable |


   @T006-Proof @normal @AcceptanceTest @Revocation
   Scenario Outline: Holder accepts the proof request of a non-revoked revokable credential where the verifier doesn't care if the credential was revoked
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |
      When the user has a proof request for <proof>
      And they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      And they select Go back to home on information sent successfully
      #And once the proof is verified they are informed of such
      #And they select Done on the verfified information
      Then they are brought Home

      Examples:
         | credential                   | proof                    |
         | cred_data_photo_id_revokable | proof_photo_id_revokable |


   # if a non-revokable credential can be presented then that should take precedent over revokable credentials since it de facto satisfies proof of non-revocation.
   @T007-Proof @normal @AcceptanceTest @Revocation
   Scenario Outline: Holder accepts the proof request of a non-revoked credential and presents a non-revokable credential
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Photo Id        |
      And the holder has another credential of <credential_2>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |
      When the user has a proof request for <proof> including proof of non-revocation at <interval>
      Then 'Photo Id' is selected as the credential to verify the proof
      Then they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      And they select Go back to home on information sent successfully
      And they are brought Home

      Examples:
         | credential         | credential_2                 | proof                                          | interval |
         | cred_data_photo_id | cred_data_photo_id_revokable | proof_photo_id_revokable_no_schema_restriction | now:now  |


   @T008-Proof @critical @AcceptanceTest @Revocation
   Scenario Outline: Holder accepts the proof request of a non-revoked credential and presents a non-revokable credential that has been revoked and reissued
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |
      And the credential has been revoked by the issuer
      When the user has a proof request for <proof> including proof of non-revocation at <interval>
      And they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      Then they are brought Home

      Examples:
         | credential                   | proof                    | interval |
         | cred_data_photo_id_revokable | proof_photo_id_revokable | now:now  |

   @T010.1-Proof @normal @MultiCredProof @AcceptanceTest @Story_614
   Scenario Outline: Holder accepts a proof request with multiple credentials
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Photo Id        |
      And the holder has another credential of <credential_2>
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Sauce Labs Test |
      When the user has a proof request for <proof>
      And the request informs them of the attributes and credentials they came from
      And they select Share
      And the holder is informed that they are sending information securely
      Then they are informed that the information sent successfully
      
      Examples:
         | credential         | credential_2              | proof             |
         | cred_data_photo_id | cred_data_sauce_labs_test | multi_cred_proof  |

   @T010.2-Proof @normal @MultiCredProof @AcceptanceTest @Story_614
   Scenario Outline: Holder declines a proof request with multiple credentials
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
      And the holder has another credential of <credential_2>
      When the user has a proof request for <proof>
      And the request informs them of the attributes and credentials they came from
      And they select Decline
      Then they are asked if they are sure they want to decline the Proof
      And they Confirm the decline
      And they are brought home

      Examples:
         | credential         | credential_2              | proof             |
         | cred_data_photo_id | cred_data_sauce_labs_test | multi_cred_proof  |

   # TODO: Update these tests when revocation messages are working with the app again 2025-04-04
   # @T010.3-Proof @normal @MultiCredProof @AcceptanceTest @Story_614 @wip
   # Scenario Outline: Holder accepts a proof request with multiple credentials, however one is revoked
   #    Given the User has completed on-boarding
   #    And the User has accepted the Terms and Conditions
   #    And a PIN has been set up with "369369"
   #    And the Holder has opted out of biometrics to unlock BC Wallet
   #    And a connection has been successfully made
   #    And the holder has a credential of <credential>
   #       | issuer_agent_type | credential_name |
   #       | TractionIssuer    | Photo Id        |
   #    And the holder has another credential of <credential_2>
   #       | issuer_agent_type | credential_name |
   #       | TractionIssuer    | Sauce Labs Test |
   #    When the user has a proof request <proof>
   #    And the request informs them of the attributes and credentials they came from
   #    And they select Share
   #    And the holder is informed that they are sending information securely
   #    Then they are informed that the information sent successfully
   #    And the proof is unverified
   
   #    Examples:
   #       | credential                   | credential_2              | proof             |
   #       | cred_data_photo_id_revokable | cred_data_sauce_labs_test | multi_cred_proof  |


   # TODO: Update these tests when revocation messages are working with the app again 2025-04-04
   # @T011.1-Proof @normal @RevocationNotification @AcceptanceTest @Story_63
   # Scenario: Holder is notified that their credential has been revoked and is acknowledged
   #    Given the User has completed on-boarding
   #    And the User has accepted the Terms and Conditions
   #    And a PIN has been set up with "369369"
   #    And the Holder has opted out of biometrics to unlock BC Wallet
   #    And that the holder has a revocable credential stored in the wallet
   #       | credential                   | revocable | issuer_agent_type | credential_name    |
   #       | cred_data_photo_id_revokable | True      | TractionIssuer    | Photo Id Revokable |
   #    When a credential has been revoked by the issuer
   #       | issuer_agent_type | credential_name |
   #       | TractionIssuer    | photo_id_revokable |
   #    Then The holder receives a revocation message notification
   #    And the holder selects the revocation notification
   #    And the holder reviews the contents of the revocation notification message
   #       | credential_name | revoked_message            |
   #       | Photo Id        | This credential is revoked |
   #    And acknowledges the revocation notification
   #    And the credential has a revoked status
   #    And the revocation notification is removed

   # TODO: Update these tests when revocation messages are working with the app again 2025-04-04
   # @T011.2-Proof @normal @RevocationNotification @AcceptanceTest @Story_63
   # Scenario: Holder of a dismissed revoked notification reviews revocation status again
   #    Given the User has completed on-boarding
   #    And the User has accepted the Terms and Conditions
   #    And a PIN has been set up with "369369"
   #    And the Holder has opted out of biometrics to unlock BC Wallet
   #    And that the holder has a revocable credential stored in the wallet
   #       | credential                | revocable | issuer_agent_type | credential_name |
   #       | cred_data_drivers_license | True      | TractionIssuer    | Drivers License |
   #    And a credential has been revoked by the issuer
   #       | issuer_agent_type | credential_name |
   #       | TractionIssuer    | drivers_license |
   #    And The holder has received and acknowledged the revocation message notification
   #    When the holder selects the credential
   #    Then they will be informed of its revoked status


   @T012.1-Proof @normal @AcceptanceTest @SelfAttestation @Story_239
   Scenario Outline: Holder accepts the proof request that contains self-attested attributes but the attribute is in an existing credential
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a credential of <credential>
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Photo Id        |
      And the holder has another credential of <credential_2>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |
      When the user has a proof request for <proof> including proof of non-revocation at <interval>
      Then they select Share
      And the holder is informed that they are sending information securely
      And they are informed that the information sent successfully
      And they select Go back to home on information sent successfully
      And they are brought Home

      Examples:
         | credential         | credential_2                 | proof                                  | interval |
         | cred_data_photo_id | cred_data_photo_id_revokable | proof_photo_id_revokable_self_attested | now:now  |