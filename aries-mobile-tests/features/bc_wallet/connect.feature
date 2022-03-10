# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/76
@Connect @bc_wallet @Story_76
Feature: Connect to an Issuer/Scan QR Code for Credential


@T001-Connect @wip @critical @AcceptanceTest
Scenario: Scan QR code to recieve a credential offer
   Given the User has completed on-boarding
   And the User has accepted the Terms and Conditions
   And a PIN has been set up with "369369"
   When the Holder scans the QR code sent by the issuer
   And the Holder is taken to the Connecting Screen/modal
   And the Connecting completes successfully
   Then there is a connection between Issuer and Holder

@T002-Connect @wip @normal @AcceptanceTest
Scenario: Scan QR code to recieve a credential offer but exits scanning

@T003-Connect @wip @minor @FunctionalTest
Scenario: Scan QR code with flash on to recieve a credential offer

