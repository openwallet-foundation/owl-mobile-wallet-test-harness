# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/29
@Proof @bc_wallet @Story_29
Feature: Proof
   In order easily prove my credential details to a verifier
   As a holder
   I want to be able to review, accept, and decline a proof request


   @T001-Proof @wip @critical @AcceptanceTest @Story_29
   Scenario: Holder receives and views the contents of a credential offer
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
         | issuer_agent_type | who         | cred_type    | attributes           | values                  |
         | AATHIssuer        | aca-py.Acme | Test Schema. | Attr 1;Attr 2;Attr 3 | value_1;value_2;value_3 |
   #| CANdyWebIssuer    | # CANdy - Unverified Person Issuer | Unverified Person | First Name;Last Name;Date of Birth;Street Address;Postal Code;City;Province;Country;Issued | Sheldon;Regular;1989-03-04;123 Perfect Street;A2V 3E1;Awesome City;BC;Canada;2022-03-14T23:27:20.133Z |


   @T002-Proof @wip @critical @AcceptanceTest @Story_29
   Scenario: Holder accepts the credential offer recieved
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And a connection has been successfully made
      And the holder has a Non-Revocable credential
      And the holder is connected to the verifier
      And the user has a proof request
      When they select Accept
      And the holder is informed that they are sending information securely
      And once the proof is verified they are informed of such
      And they select Done
      Then they are brought Home
         | issuer_agent_type | credential_name |
         | AATHIssuer        | Test Schema     |

