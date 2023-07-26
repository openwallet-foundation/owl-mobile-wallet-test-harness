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
         | issuer_agent_type | credential_name  |
         | BCVPIssuer        | Pilot Invitation |
      And they are Home
      When they select to start getting the Person credential
      And they select Get your Person credential
      And they select Log in with BC Services Card in the Create a BC Digital ID Web page
      And they select <setup_option> on the Set up the BC Services Card app
      And they enter in <username> as the username
      And they enter in <password> as the password
      And they select I agree on the Review page
      And they select Send Credential
      And they select Accept
      And the holder is informed that their credential is on the way with an indication of loading
      And once the credential arrives they are informed that the Credential is added to your wallet
      And they select Done
      Then the credential accepted is at the top of the list
         | issuer_agent_type | credential_name |
         | BCVPIssuer        | Person          |
      And the BCVC Pilot credential is after the IDIM Person credential
         | issuer_agent_type | credential_name  |
         | BCVPIssuer        | Pilot Invitation |

      # username and passwords are pointers to env vars that hold the actual values
      Examples:
         | setup_option                    | username          | password              |
         | Test with username and password | BCSC_ACCOUNT_USER | BCSC_ACCOUNT_PASSWORD |
#         | BC Services Card app            | BCSC_ACCOUNT_USER | BCSC_ACCOUNT_PASSWORD |


   @T002-BCSC @critical @AcceptanceTest
   Scenario Outline: BCSC holder aquires the BC Person Credential and uses it in a Proof
      Given the BCSC holder has setup thier Wallet
      And the BCSC holder has a <credential>
         | issuer_agent_type | credential_name  |
         | BCVPIssuer        | Pilot Invitation |
      And the BCSC holder has the BC Person Credential with <setup_option>, <username>, and <password>
         | issuer_agent_type | credential_name |
         | BCVPIssuer        | Person          |
      When the user has a proof request
      And they select Share
      And the holder is informed that they are sending information securely
      Then they are informed that the information sent successfully
      #And the verifier reports a successful proof
      #And they select Go back to home on information sent successfully
      #Then they are brought Home

      # username and passwords are pointers to env vars that hold the actual values
      Examples:
         | setup_option                    | username          | password              |
         | Test with username and password | BCSC_ACCOUNT_USER | BCSC_ACCOUNT_PASSWORD |

   @T00X-BCSC @Normal @FunctionalTest @wip
   Scenario: BCSC holder removes the IDIM Person credential and can get the IDIM credential again with the button on the home page

   @T00X-BCSC @Normal @FunctionalTest @wip
   Scenario: BCSC holder removes the IDIM Person credential and the BCVC Certificate and can get the IDIM credential again repeating the credential request