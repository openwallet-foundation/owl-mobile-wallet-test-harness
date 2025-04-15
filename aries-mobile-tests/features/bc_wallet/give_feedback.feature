# https://github.com/bcgov/bc-wallet-mobile/issues/1002
#TODO: this test needs to be fixed
@GiveFeedback 
Feature: Give Feedback
  In order to communicate concerns, issues, and praise
  As a wallet user
  I want to be able to give feedback easily in the app


  @T001-GiveFeedback @AcceptanceTest
  Scenario Outline: Wallet user gives feedback
    Given the wallet user <user_state>
    And they are on on the landing page
    When they select Give Feedback
    Then they are taken to the Feedback form

    Examples:
      | user_state         |
      | has just onboarded |
#| reopens the app                    |
#| has just recieved a credential     |
#| has just completed a proof request |