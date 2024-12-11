@TermsAndConditionsQC @qc_wallet @normal
Feature: Terms and Conditions
  In order to understand my legal obligations when using the app
  As a new holder, i want to review the terms and conditions

@T001-TandC @AcceptanceTest @normal
Scenario: New User Accepts Terms and Conditions
Given the User is on the Terms and Conditions screen
When the users accepts the Terms and Conditions
And the user clicks continue
Then the user transitions to the PIN creation screen

@T002-TandC @AcceptanceTest @normal
Scenario: New User Accepts Terms and Conditions
Given the User is on the Terms and Conditions screen
When the user clicks continue without accepting the Terms and Conditions
Then the user is on the Terms and Conditions screen
