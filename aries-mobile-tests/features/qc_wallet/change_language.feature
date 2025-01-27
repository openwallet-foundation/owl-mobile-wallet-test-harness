@Language @qc_wallet @normal
Feature: Language
  In order to use the app in my preferred language
  As a holder
  I want to be able to change the language of the app

  @T001.1-Language @AcceptanceTest @extra_config_language_1 
  Scenario: Existing holder changes language from English to French
    Given the holder has initially selected "English" as the language
    And the holder open the Application settings page
    When the holder changes app language to "French"
    Then the language changes automatically to "French"

  @T002.1-Language @FunctionalTest @extra_config_language_1
  Scenario: Holder quits app after changing language
    Given the holder has initially selected "English" as the language
    And the holder open the Application settings page
    And they have selected "French"
    Then the language changes automatically to "French"
    When they have closed the app
    And they relaunch the app
    Then the language is set to "French"

  @T001.2-Language @AcceptanceTest @extra_config_language_2
  Scenario: Existing holder changes language from French to English
    Given the holder has initially selected "French" as the language
    And the holder open the Application settings page
    When the holder changes app language to "English"
    Then the language changes automatically to "English"

  @T002.2-Language @FunctionalTest @extra_config_language_2
  Scenario: Holder quits app after changing language
    Given the holder has initially selected "French" as the language
    And the holder open the Application settings page
    And they have selected "English"
    Then the language changes automatically to "English"
    When they have closed the app
    And they relaunch the app
    Then the language is set to "English"