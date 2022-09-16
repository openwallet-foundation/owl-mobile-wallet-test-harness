# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/hyperledger/aries-mobile-agent-react-native/148
@TermsAndConditions @bc_wallet @Story_148 @normal
Feature: Terms and Conditions
  In order to understand my legal obligations when using the app
  As a new holder
  I want to review the terms and conditions

@T001-TandC @AcceptanceTest @normal
Scenario: New User Accepts Terms and Conditions
Given the User has completed on-boarding
And the User is on the Terms and Conditions screen
When the users accepts the Terms and Conditions
And the user clicks continue
Then the user transitions to the PIN creation screen

@T002-TandC @AcceptanceTest @normal
Scenario: New User Rejects Terms and Conditions
Given the User has completed on-boarding
And the User is on the Terms and Conditions screen
When the User presses the back button
Then the User goes back to the last on-boarding screen they viewed

@T003-TandC @FunctionalTest @low
Scenario: New User Rejects Terms and Conditions and returns to app to accept
Given the User has completed on-boarding
And the User was on the Terms and Conditions screen
And the user has pressed the back button
And the user was taken back to the on-boarding screen
When they have closed the app
And they relaunch the app
Then they can accept the Terms and conditions

# This is a content test, may be worth while autoamting once the text solidifies but would be fragile otherwise. 
# @T004-TandC @wip @AcceptanceTest @low @Story_118 @content
# Given the User has completed on-boarding
# When the User is on the Terms and Conditions Screen
# Then the Holder is presented with content that matches exactly the terms and conditions within the following document: 
# https://app.zenhub.com/files/429950091/85f29998-e55e-417e-a8c0-b00531b3caba/download