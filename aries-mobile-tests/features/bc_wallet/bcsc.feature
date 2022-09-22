# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/407
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/241
@BCSC @bc_wallet @Story_29
Feature: BCSC
   In order to easily prove I hold a BCSC
   As a BCSC holder
   I want to be able to store and use my BCSC in my BC Wallet


   @T001-BCSC @critical @AcceptanceTest
   Scenario Outline: BCSC holder aquires BC VC Certificate that in turn allows them to store the BCSC in the BC Wallet
      Given the BCSC holder has setup thier Wallet
      And the BCSC holder has a <credential>
         | issuer_agent_type | credential_name         |
         | BCVCIssuer        | BC VC Pilot Certificate |
      # And the Issuer selects New Invite
      # And the issuer fills out email, name, and program of IDIM Testing
      # And the issuer clicks invite
      # And the BCSC holder opens thier email and clicks the invite link
      # And they check agree and select agree (has to be on a device that has access to bcvc pilot)
      # And the Holder select Request Credential
      # And they select I confirm and agree
      # And they scan the QR Code presented
      # And the Holder selects accept in the app
      # and they recieve the credential
      And they are Home
      When they select Get your BC Digital ID
      And they select Share on the proof request from IDIM
      And they select Log in with BC Services Card in the Create a BC Digital ID Web page
      And they select <setup_option> on the Set up the BC Services Card app
      And they enter in the <card_serial_number>
      And they enter in the <passcode>
      And they select I agree on the Review web page
      And they select Send Credential
      Then they get are told Your Credential has been Issued
      And they Close and go to Wallet (select home for now)
      And they select View on the new Credential Offer
      And they select Accept on the IDIM Credential
      And the credential is on the way
      And the credential is added to your wallet
      And they select Done
      And the IDIM Person credential is added at the top
      And the BCVC Pilot credential is after the IDIM Person credential

      Examples:
         | setup_option    | card_serial_number | passcode |
         | Virtual testing | Wallet03           | 2022     |

   @T00X-BCSC @Normal @FunctionalTest
   Scenario: BCSC holder removes the IDIM Person credential and can get the IDIM credential again with the button on the home page

   @T00X-BCSC @Normal @FunctionalTest
   Scenario: BCSC holder removes the IDIM Person credential and the BCVC Certificate and can get the IDIM credential again repeating the credential request