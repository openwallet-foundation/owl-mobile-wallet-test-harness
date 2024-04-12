@CredentialOffer @qc_wallet @Story_81
Feature: Offer a Credential
   In order have confidence and control of my wallet
   As a holder
   I want to be able to review, accept, and decline a credential offer


   @T001.1-CredentialOffer @critical @AcceptanceTest @Story_79
   Scenario: Holder receives and views the contents of a credential offer
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the User allows notifications
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      When the Holder receives a Non-Revocable credential offer
      And the holder opens the credential offer
      Then holder is brought to the credential offer screen
      And they can view the contents of the credential
         | issuer_agent_type | who         | cred_type    | attributes           | values                  |
         | MCNIssuer         | aca-py.Acme | Test Schema  | Attr 1;Attr 2;Attr 3 | value_1;value_2;value_3 |
   #| CANdyWebIssuer    | # CANdy - Unverified Person Issuer | Unverified Person | First Name;Last Name;Date of Birth;Street Address;Postal Code;City;Province;Country;Issued | Sheldon;Regular;1989-03-04;123 Perfect Street;A2V 3E1;Awesome City;BC;Canada;2022-03-14T23:27:20.133Z |

   @T003.1-CredentialOffer @critical @AcceptanceTest
   Scenario: Holder declines the credential offer recieved
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer
      When they select Decline the credential
      Then they are brought Home
      # Then they are brought to the list of credentials
      # And a temporary notification will appear that informs the holder of the declined action
      # And the credential declined is not in the list
      # Then the holder will be taken to the credential list page
      # And a temporary notification will appear that informs the holder of the declined action
      #
