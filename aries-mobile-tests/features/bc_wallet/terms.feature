# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/hyperledger/aries-mobile-agent-react-native/148
@TermsAndConditions @bc_wallet @Story_148 @normal
Feature: Terms and Conditions
  In order to understand my legal obligations when using the app
  As a new holder
  I want to review the terms and conditions

@T001-T&C @wip @AcceptanceTest
Scenario: New User Accepts Terms and Conditions
Given The User has completed the on-boarding carousel screens
And User sees the Terms and Conditions screen
When The User scrolls to the bottom of the screen
And The users accepts the Terms and Conditions
And The continue button becomes active
And The user clicks continue
Then The user transitions to the PIN creation screen

@T002-T&C @wip @AcceptanceTest
Scenario: New User Rejects Terms and Conditions
Given The User has completed the on-boarding carousel screens
And User sees the Terms and Conditions screen
When The User scrolls to the bottom of the screen
And The User presses the back button
Then The User goes back to the last on-boarding screen they viewed

@T003-T&C @wip @FunctionalTest
Scenario: New User Rejects Terms and Conditions and returns to app to accept
Given The User has completed the on-boarding carousel screens
And User sees the Terms and Conditions screen
And the user has pressed that back button
And the user was taken back to the on-bording screen
When they close the app
And they reopen the app
Then they can accept the Terms and conditions