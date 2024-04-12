# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/74
@Language @bc_wallet @qc_wallet @Story_74 @normal
Feature: Language
  In order to use the app in my preferred language
  As a holder
  I want to be able to change the language of the app

  @T001.1-Language @AcceptanceTest @extra_config_language_1
  Scenario: Existing holder changes language from English to French
    Given the holder has initially selected "English" as the language
    And the holder is in the language settings
    When the holder changes app language to "French"
    Then the language changes automatically to "French"

  @T001.2-Language @AcceptanceTest @extra_config_language_2
  Scenario: Existing holder changes language from French to English
    Given the holder has initially selected "French" as the language
    And the holder is in the language settings
    When the holder changes app language to "English"
    Then the language changes automatically to "English"


  @T002.1-Language @FunctionalTest @extra_config_language_1
  Scenario: Holder quits app after changing language
    Given the holder has initially selected "English" as the language
    And the holder is in the language settings
    And they have selected "French"
    Then the language changes automatically to "French"
    When they have closed the app
    And they relaunch the app
    Then the language is set to "French"

  @T002.2-Language @FunctionalTest @extra_config_language_2
  Scenario: Holder quits app after changing language
    Given the holder has initially selected "French" as the language
    And the holder is in the language settings
    And they have selected "English"
    Then the language changes automatically to "English"
    When they have closed the app
    And they relaunch the app
    Then the language is set to "English"


  # @T00X-Language @wip @OutOfScope
  # Scenario Outline: New User sets intial language
  #   Given the new user has opened the app for the first time
  #   And they are in the initial select language screen
  #   When the new user selects <language>
  #   Then the new user is brought to the onboarding screen in the <language> they selected
  #
  #   Examples:
  #     | language |
  #     | English  |
  #     | French   |
