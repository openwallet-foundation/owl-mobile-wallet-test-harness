# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/hyperledger/aries-mobile-agent-react-native/146
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/93
@SecureWallet @bc_wallet @Story_146 @Story_93 @normal
Feature: Secure your Wallet
  In order to be reassured that my digital wallet will not be used maliciously
  As a person who is curious but cautious of digital wallets
  I want to set my security settings to maximum security

# Secure your Wallet has not been implemented in the BC wallet yet. 
# Adding a pin entry process to get through to other fucntionality.

@T001-SecureWallet @wip @TemporaryTest @normal
Scenario: New User Sets Up PIN
Given the User has completed on-boarding
And the User has accepted the Terms and Conditions
And the User is on the PIN creation screen
When the User enters the first PIN as "369369"
And the User re-enters the PIN as "369369"
And the User selects Create PIN
Then the User has successfully created a PIN
And they land on the Home screen

