# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/hyperledger/aries-mobile-agent-react-native/148
@TermsAndConditions @bc_wallet @Story_148 @normal
Feature: Terms and Conditions
  In order to understand my legal obligations when using the app
  As a new holder
  I want to review the terms and conditions

@T001-TandC @AcceptanceTest
Scenario: New User Accepts Terms and Conditions
Given the User has completed on-boarding
And the User is on the Terms and Conditions screen
When the User scrolls to the bottom of the screen
And the users accepts the Terms and Conditions
And the user clicks continue
Then the user transitions to the PIN creation screen

@T002-TandC @AcceptanceTest
Scenario: New User Rejects Terms and Conditions
Given the User has completed on-boarding
And the User is on the Terms and Conditions screen
When the User scrolls to the bottom of the screen
And the User presses the back button
Then the User goes back to the last on-boarding screen they viewed

@T003-TandC @wip @FunctionalTest
Scenario: New User Rejects Terms and Conditions and returns to app to accept
Given the User has completed on-boarding
And the User was on the Terms and Conditions screen
And the user has pressed the back button
And the user was taken back to the on-bording screen
When they close the app
And they reopen the app
Then they can accept the Terms and conditions