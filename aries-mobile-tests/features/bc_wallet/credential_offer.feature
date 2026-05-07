# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/81
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/79
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/82
@CredentialOffer @bc_wallet @Story_81
Feature: Offer a Credential
   In order have confidence and control of my wallet
   As a holder
   I want to be able to review, accept, and decline a credential offer


   @T001-CredentialOffer @critical @AcceptanceTest @Story_79
   Scenario: Holder receives and views the contents of a credential offer
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      When the Holder receives a Non-Revocable credential offer
      And the holder opens the credential offer
      Then holder is brought to the credential offer screen
      And they can view the contents of the credential offer
         | issuer_agent_type | who                   | cred_type   | attributes           | values     |
         | TractionIssuer    | Sauce labs Connection | Test Schema | first_name;last_name | Sauce;Test |
   #| CANdyWebIssuer    | # CANdy - Unverified Person Issuer | Unverified Person | First Name;Last Name;Date of Birth;Street Address;Postal Code;City;Province;Country;Issued | Sheldon;Regular;1989-03-04;123 Perfect Street;A2V 3E1;Awesome City;BC;Canada;2022-03-14T23:27:20.133Z |


   @T002-CredentialOffer @critical @AcceptanceTest @Story_79 @Story_82
   Scenario: Holder accepts the credential offer received
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer
      When they select Accept
      And the holder is informed that their credential is on the way with an indication of loading
      And once the credential arrives they are informed that the Credential is added to your wallet
      And they select Done
      Then they are brought to the list of credentials
      And the credential accepted is at the top of the list
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Sauce Labs Test |

   @T002.1-CredentialOffer @critical @AcceptanceTest @Story_79 @Story_82
   Scenario Outline: Holder accepts the credential offer received
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer of <credential>
      When they select Accept
      And the holder is informed that their credential is on the way with an indication of loading
      And once the credential arrives they are informed that the Credential is added to your wallet
      And they select Done
      Then they are brought to the list of credentials
      And the credential accepted is at the top of the list
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Photo Id        |

      Examples:
         | credential         |
         | cred_data_photo_id |


   @T003-CredentialOffer @critical @AcceptanceTest @Story_79
   Scenario: Holder declines the credential offer received
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer
      When the holder see the credential offer
      And the user delinces the credential offer
      And the user deletes credential offer
      Then they have access to the app

   # @T006-CredentialOffer @wip @critical @AcceptanceTest @Story_79 @Story_82
   # Scenario: Holder accepts the credential offer recieved with previous credential(s)
   #    Given the User has completed on-boarding
   #    And the User has accepted the Terms and Conditions
   #    And a PIN has been set up with "369369"
   #    And the Holder has opted out of biometrics to unlock BC Wallet
   #    And a connection has been successfully made
   #    And the user has existing credentials
   #    And the user has a credential offer
   #    When they select Accept
   #    And the holder is informed that their credential is on the way with an indication of loading
   #    And once the credential arrives they are informed that the Credential is added to your wallet
   #    And they select Done
   #    Then they are brought to the list of credentials
   #    And the credential accepted is at the top of the list



   @T004-CredentialOffer @normal @FunctionalTest @PerformanceTest
   Scenario Outline: Holder multiple credentials and no issuance should take a long time
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      And a connection has been successfully made
      When the Holder receives a Non-Revocable credential offer
      When the Holder receives a credential offer of <credential>
         | issuer_agent_type | credential_name |
         | TractionIssuer    | Photo Id        |
      When the Holder receives a credential offer of <credential_2>
         | issuer_agent_type | credential_name    |
         | TractionIssuer    | Photo Id Revokable |

      Examples:
         | credential         | credential_2                |
         | cred_data_photo_id | cred_data_photo_id_revokable |


   # @T005-CredentialOffer @normal @AcceptanceTest @Connectionless @PerformanceTest
   # Scenario Outline: Pan Canadian Trust Framework Member issued multiple Unverified Person Credentials and no issuance should talke a long time
   #    Given the PCTF Member has setup thier Wallet
   #    And the PCTF member has an Unverified Person <credential>
   #       | issuer_agent_type | credential_name   |
   #       | CANdyUVPIssuer    | Person |
   #    And the PCTF member has an Unverified Person <credential>
   #       | issuer_agent_type | credential_name   |
   #       | CANdyUVPIssuer    | Person |
   #    And the PCTF member has an Unverified Person <credential>
   #       | issuer_agent_type | credential_name   |
   #       | CANdyUVPIssuer    | Person |


   #    Examples:
   #       | credential                  |
   #       | cred_data_unverified_person |