@Onboarding @qc_wallet @normal
Feature: Onboarding
  In order to understand how the app works
  As a new holder
  I want to review onboarding material


  @T001-Onboarding @AcceptanceTest
  Scenario: New User reviews all onboarding screens
    Given the new user has opened the app for the first time
    And the user is on the onboarding Welcome screen
    When the user selects Next
    And they are brought to the Store your credentials securely screen
    And the user selects Next
    And they are brought to the Share only what is neccessary screen
    And the user selects Next
    And they are brought to the Take control of your information screen
    Then they can select Get started
    And are brought to the Terms and Conditions screen


  @T002-Onboarding @AcceptanceTest
  Scenario Outline: New User skips onboarding screens
    Given the new user has opened the app for the first time
    And the user is on the onboarding <screen>
    When the user selects Skip
    Then are brought to the Terms and Conditions screen

    Examples:
      | screen                                 |
      | Welcome screen                         |
      | Store your credentials securely screen |
      | Share only what is neccessary screen   |


  @T003-Onboarding @AcceptanceTest
  Scenario Outline: New User wants to go back to review previous reviewed onboarding material
    Given the new user has opened the app for the first time
    And the user is on the onboarding <screen>
    When the user selects Back
    Then are brought to the <previous_screen>

    Examples:
      | screen                                  | previous_screen                        |
      | Store your credentials securely screen  | Welcome screen                         |
      | Share only what is neccessary screen    | Store your credentials securely screen |
      | Take control of your information screen | Share only what is neccessary screen   |


  @T004-Onboarding @FunctionalTest
  Scenario Outline: New User quits app mid review of onboarding material
    Given the new user has opened the app for the first time
    And the user is on the onboarding <screen>
    When they have closed the app
    And they relaunch the app
    Then they land on the Welcome screen

    Examples:
      | screen                                 |
      | Welcome screen                         |
      | Store your credentials securely screen |
      | Share only what is neccessary screen   |
      | Take control of your information screen |
