@Security @qc_wallet
Feature: Secure your Wallet
  In order to be reassured that my digital wallet will not be used maliciously
  As a person who is curious but cautious of digital wallets
  I want to set my security settings to maximum security

  @TCL_PNG_ACC_002.1 @FunctionalTest @ExceptionTest @normal
  Scenario Outline: New User Sets Up PIN but does not follow conventions
    Given the User has skipped on-boarding
    And the User has accepted the Terms and Conditions
    And the User is on the PIN creation screen
    When the User enters the first PIN as <pin>
    And the User re-enters the PIN as <pin> 
    And the User selects Create PIN
    Then they are informed of <pin_error> 
    And they select ok on PINs error

    Examples:
      | pin    | pin_error                                                            |
      | @28193 | Your PIN needs to only contain digits. Please try again.             |
      | D28193 | Your PIN needs to only contain digits. Please try again.             |
      | 123893 | A series was detected in your PIN. Please try again.                 |
      | 333752 | The PIN can't have a repetition of the same digit. Please try again. |
      | 65237  | Your PIN is too short. Please try again.                             |

  @TCL_PNG_ACC_002.2 @FunctionalTest @ExceptionTest @normal
  Scenario: New User Sets Up PIN and checks pin by toggling visibility
    Given the User has skipped on-boarding
    And the User has accepted the Terms and Conditions
    And the User is on the PIN creation screen
    When the User enters the first PIN as "728193"
    Then they select visibility toggle on the first PIN as "728193"
    When the User re-enters the PIN as "278596"
    Then they select visibility toggle on the second PIN as "278596"

  @TCL_PNG_ACC_009 @FunctionalTest @extra_config_security_idle_timeout
  Scenario: Holder has app locked after 5 minutes of inactivity
    Given the Holder has setup thier Wallet
    And the Holder has selected to use PIN only to unlock BC Wallet
    Then they land on the Home screen
    When the Holder stops interacting with the app 
    Then the app is locked for security reasons and a message is shown to the Holder
      | lock_time | lock_message      |
      | 300       | You're logged out |

    


