# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/74
@Language @bc_wallet @Story_74 @normal
Feature: Language
  In order to use the app in my preferred language
  As a holder
  I want to be able to change the language of the app


  @T001-Language @wip @AcceptanceTest
  Scenario Outline: Existing holder changes language
    Given the holder has initially selected <language> as the language
    And the holder is in the language settings
    When the ID holder selects <different language>
    Then the language changes automatically to <different language>

    Examples:
      | language | different language |
      | English  | French             |
      | French   | English            |


  @T002-Language @wip @FunctionalTest
  Scenario Outline: Holder quits app after changing language
    Given the holder has initially selected <language> as the language
    And the holder is in the language settings
    And they have selected a <different language>
    When they quit the app
    And they reopen the app
    Then the language is set to <different language>

    Examples:
      | language | different language |
      | English  | French             |
      | French   | English            |



  @T00X-Language @wip @OutOfScope
  Scenario Outline: New User sets intial language
    Given the new user has opened the app for the first time
    And they are in the initial select language screen
    When the new user selects <language>
    Then the new user is brought to the onboarding screen in the <language> they selected

    Examples:
      | language |
      | English  |
      | French   |