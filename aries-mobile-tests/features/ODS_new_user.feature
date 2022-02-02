#DID-349 , 351, 352
Feature: Explainer screens

  Background: I am a new user and wallet is not setup
    Given I am a new user 
    And My wallet is not setup

  @DID-372
  Scenario: New user navigates to device's security settings
    Given I am on Get started screen
    When I click on Check your device's security settings 
    Then I land on Device settings screen 

  @DID-
  Scenario: New user reviews all explainer screens 
    Given My langauage has been set 
    And I am on Get started screen
    When I click on Get started 
    And I accept Terms of service
    And I click Continue on Terms of Use 
    And I land on Store credentials screen
    And I click Next 
    And I land on Share only necessary screen
    And I click Next 
    And I land on Keep track of what you shared screen
    And I click Done 
    Then I am on Confirm your biometircs screen 

  @DID- 
  Scenario Outline: New user skips explainer screens
    Given My langauage has been set 
    And I am on Get started screen
    And I clicked on Get started 
    And I am on the explanier <screen>
    When I click Skip 
    Then I land on Confirm your biometrics screen 

    Examples:
    |screen|
    |Store credentials screen|
    |Share only necessary screen|
    |Keep track of what you shared screen|

@DID-?
  Scenario: New user wants to review previous explanier screen 
    Given My langauage has been set 
    And I am on Get started screen
    And I clicked on Get started 
    And I am on the explanier <screen>
    When the user selects Back
    Then I am on the explainer <previous screen>

    Examples:
    |screen                                 |previous screen           |
    |Store credentials screen               |Terms of use screen       |
    |Share only necessary screen            |Store credentials screen  |
    |Keep track of what you shared screen   |Share only necessary screen |
