# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/81
@CredentialOffer @bc_wallet @Story_81
Feature: Issuer Offers a Credential


   @T001-CredentialOffer @critical @AcceptanceTest
   Scenario: Holder receives and views the contents of a credential offer
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And a connection has been successfully made
      When the Holder receives a Non-Revocable credential offer
      And the Holder taps on the credential offer notification
      Then holder is brought to the credential offer screen
      And they can view the contents of the credential
         | issuer_agent_type | who                                | cred_type         | attributes                                                                                 | values                                                                                                |
         | AATHIssuer        | aca-py.Acme                        | Test Schema.      | Attr 1;Attr 2;Attr 3                                                                       | value_1;value_2;value_3                                                                               |
         #| CANdyWebIssuer    | # CANdy - Unverified Person Issuer | Unverified Person | First Name;Last Name;Date of Birth;Street Address;Postal Code;City;Province;Country;Issued | Sheldon;Regular;1989-03-04;123 Perfect Street;A2V 3E1;Awesome City;BC;Canada;2022-03-14T23:27:20.133Z |


# Should these be in a different feature file?
#AND see a button to accept the credential
#AND see a button to decline the credential


