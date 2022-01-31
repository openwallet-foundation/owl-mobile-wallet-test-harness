# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/8
@Onboarding @bc_wallet @Story_8 @normal
Feature: Onboarding
  In order to understand how the app works
  As a new holder
  I want to review onboarding material

@T001-Onboarding @wip @AcceptanceTest
Scenario: New User reviews all onboarding screens
Given The User has completed the on-boarding carousel screens
And User sees the Terms and Conditions screen
When The User scrolls to the bottom of the screen
And The users accepts the Terms and Conditions
And The continue button becomes active
And The user clicks continue
Then The user transitions to the PIN creation screen

@T002-Onboarding @wip @AcceptanceTest
Scenario: New User wants to go back to review previous reviewed onboarding material

@T003-Onboarding @wip @FunctionalTest
Scenario: New User quits app mid review of onboarding material