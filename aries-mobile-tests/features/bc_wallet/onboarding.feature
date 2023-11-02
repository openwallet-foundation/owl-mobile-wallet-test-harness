# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/1497
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/8
@Onboarding @bc_wallet @Story_8 @Story_1497 @normal
Feature: Onboarding
  In order to understand how the app works
  As a new holder
  I want to review onboarding material


  @T001-Onboarding @AcceptanceTest
  Scenario: New User reviews all onboarding screens
    Given the new user has opened the app for the first time
    And the user is on the Is this app for you screen
    When the user selects confirms that the app is for them
    And they select Continue
    And they are brought to the A different smart wallet screen
    And the user selects Next
    And they are brought to the Digital credentials screen
    And the user selects Next
    And they are brought to the Private and confidential screen
    Then they can select Get started
    And are brought to the Terms and Conditions screen


  @T002-Onboarding @AcceptanceTest
  Scenario Outline: New User skips onboarding screens
    Given the new user has opened the app for the first time
    And the user is on the Is this app for you screen
    And the user selects confirms that the app is for them
    And they select Continue
    And the user is on the onboarding <screen>
    When the user selects Skip
    Then are brought to the Terms and Conditions screen

    Examples:
      | screen                          |
      | A different smart wallet screen |
      | Digital credentials screen      |


  @T003-Onboarding @AcceptanceTest
  Scenario Outline: New User wants to go back to review previous reviewed onboarding material
    Given the new user has opened the app for the first time
    And the user is on the Is this app for you screen
    And the user selects confirms that the app is for them
    And they select Continue
    And the user is on the onboarding <screen>
    When the user selects Back
    Then are brought to the <previous_screen>

    Examples:
      | screen                          | previous_screen                 |
      | Digital credentials screen      | A different smart wallet screen |
      | Private and confidential screen | Digital credentials screen      |


  @T004-Onboarding @FunctionalTest
  Scenario Outline: New User quits app mid review of onboarding material
    Given the new user has opened the app for the first time
    And the user is on the Is this app for you screen
    And the user selects confirms that the app is for them
    And they select Continue
    And the user is on the onboarding <screen>
    When they have closed the app
    And they relaunch the app
    Then they land on the A different smart wallet screen

    Examples:
      | screen                          |
      | A different smart wallet screen |
      | Digital credentials screen      |
      | Private and confidential screen |