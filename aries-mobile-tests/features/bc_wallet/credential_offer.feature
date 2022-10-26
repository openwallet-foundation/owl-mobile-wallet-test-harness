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
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      When the Holder receives a Non-Revocable credential offer
      Then holder is brought to the credential offer screen
      And they can view the contents of the credential
         | issuer_agent_type | who         | cred_type    | attributes           | values                  |
         | AATHIssuer        | aca-py.Acme | Test Schema. | Attr 1;Attr 2;Attr 3 | value_1;value_2;value_3 |
   #| CANdyWebIssuer    | # CANdy - Unverified Person Issuer | Unverified Person | First Name;Last Name;Date of Birth;Street Address;Postal Code;City;Province;Country;Issued | Sheldon;Regular;1989-03-04;123 Perfect Street;A2V 3E1;Awesome City;BC;Canada;2022-03-14T23:27:20.133Z |


   @T002-CredentialOffer @critical @AcceptanceTest @Story_79 @Story_82
   Scenario: Holder accepts the credential offer recieved
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer
      When they select Accept
      And the holder is informed that their credential is on the way with an indication of loading
      And once the credential arrives they are informed that the Credential is added to your wallet
      And they select Done
      Then they are brought to the list of credentials
      And the credential accepted is at the top of the list
         | issuer_agent_type | credential_name                           |
         | AATHIssuer        | Default AATH Issuer Credential Definition |

   @T002.1-CredentialOffer @critical @AcceptanceTest @Story_79 @Story_82
   Scenario Outline: Holder accepts the credential offer recieved
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer of <credential>
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


   @T003-CredentialOffer @wip @critical @AcceptanceTest @Story_79
   Scenario: Holder declines the credential offer recieved
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer
      When they select Decline
      Then they are brought to the list of credentials
      And a temporary notification will appear that informs the holder of the declined action
      And the credential declined is not in the list
      Then the holder will be taken to the credential list page
      And a temporary notification will appear that informs the holder of the declined action

   @T004-CredentialOffer @Story_82 @wip @ExceptionTest
   Scenario Outline: Holder is waiting for a Credential Offer but it fails to be recieved
      Given a credential offer has been received
      And accepted
      When the credential fails to be delivered to the user for <reason>
      Then a temporary error notification (toast) is displayed <error message>
      And they are taken back home
      #Then a full screen modal is displayed with an error message and a button back to the home screen?

      Examples:
         | reason                                     | error message                |
         | timeout?                                   | this is taking too long man! |
         | no internet connectivity at point of scan? | No internet                  |
         | what other reasons?                        | I don't know                 |


   @T005-CredentialOffer @Story_82 @wip @ExceptionTest
   Scenario Outline: Holder is waiting for a Credential Offer but it fails to be recieved when the user is no longer in the credential offer workflow
      Given a credential offer has been received
      And accepted
      When the holder <leaves the flow>
      When the credential fails to be delivered to the user for <reason>
      Then a temporary error notification (toast) is displayed <error message> when the user returns to the app

      Examples:
         | leaves the flow           |
         | clicks on the home button |
         | leaves the app            |

   @T006-CredentialOffer @wip @critical @AcceptanceTest @Story_79 @Story_82
   Scenario: Holder accepts the credential offer recieved with previous credential(s)
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has existing credentials
      And the user has a credential offer
      When they select Accept
      And the holder is informed that their credential is on the way with an indication of loading
      And once the credential arrives they are informed that the Credential is added to your wallet
      And they select Done
      Then they are brought to the list of credentials
      And the credential accepted is at the top of the list


   @T007-CredentialOffer @wip @critical @AcceptanceTest @Story_79
   Scenario: Holder receives and views the contents of a credential offer but takes longer that usual and gets notification on home screen
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      When the Holder receives a Non-Revocable credential offer
      And it takes longer than expected
      And they go home
      And they receive a credential offer notification
      And the Holder taps on the credential offer notification
      Then holder is brought to the credential offer screen
      And they can view the contents of the credential
         | issuer_agent_type | who         | cred_type    | attributes           | values                  |
         | AATHIssuer        | aca-py.Acme | Test Schema. | Attr 1;Attr 2;Attr 3 | value_1;value_2;value_3 |


   @T008-CredentialOffer @normal @FunctionalTest @PerformanceTest
   Scenario Outline: Holder multiple credentials and no issuance should talke a long time
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the holder has a Non-Revocable credential
         | issuer_agent_type | credential_name                           |
         | AATHIssuer        | Default AATH Issuer Credential Definition |
      And the holder has another credential of <credential>
         | issuer_agent_type | credential_name |
         | AATHIssuer        | Photo Id        |
      And the holder has another credential of <credential_2>
         | issuer_agent_type | credential_name    |
         | AATHIssuer        | Photo Id Revokable |

      Examples:
         | credential         | credential_2                |
         | cred_data_photo_id | cred_data_photo_id_revokable |


   @T009-CredentialOffer @normal @AcceptanceTest @Connectionless @PerformanceTest
   Scenario Outline: Pan Canadian Trust Framework Member issued multiple Unverified Person Credentials and no issuance should talke a long time
      Given the PCTF Member has setup thier Wallet
      And the PCTF member has an Unverified Person <credential>
         | issuer_agent_type | credential_name   |
         | CANdyUVPIssuer    | Person |
      And the PCTF member has an Unverified Person <credential>
         | issuer_agent_type | credential_name   |
         | CANdyUVPIssuer    | Person |
      And the PCTF member has an Unverified Person <credential>
         | issuer_agent_type | credential_name   |
         | CANdyUVPIssuer    | Person |


      Examples:
         | credential                  |
         | cred_data_unverified_person |