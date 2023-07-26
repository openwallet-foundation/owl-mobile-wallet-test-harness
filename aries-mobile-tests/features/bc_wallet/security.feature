# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/hyperledger/aries-mobile-agent-react-native/146
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/93
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/421
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/426
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/425
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/422
@Security @bc_wallet
Feature: Secure your Wallet
  In order to be reassured that my digital wallet will not be used maliciously
  As a person who is curious but cautious of digital wallets
  I want to set my security settings to maximum security

  @T001-Security @critical @AcceptanceTest @Story_421
  Scenario: Holder chooses biometrics and reopens to biometrics authentication
    Given the Holder has setup biometrics on thier device
    And the Holder has setup thier Wallet
    And the Holder has selected to use biometrics to unlock BC Wallet
    And they have closed the app
    When they relaunch the app
    And authenticates with thier biometrics
    Then they have access to the app


  @T002-Security @critical @AcceptanceTest @ExceptionTest @Story_? @allure.issue:https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/589
  Scenario: Holder chooses biometrics and reopens to biometrics authentication but fails once
    Given the Holder has setup biometrics on thier device
    And the Holder has setup thier Wallet
    And the Holder has selected to use biometrics to unlock BC Wallet
    And they have closed the app
    When they relaunch the app
    And fails to authenticate with thier biometrics once
    #And authenticates with thier biometrics
    And they enter thier PIN as "369369"
    Then they have access to the app


  @T003-Security @critical @AcceptanceTest @ExceptionTest @Story_426 @wip
  Scenario: Holder has multiple failed attempts to authenticate the app
    Given the Holder has setup biometrics on thier device
    And the Holder has setup thier Wallet
    And the Holder has selected to use biometrics to unlock BC Wallet
    And they have closed the app
    When they relaunch the app
    And there are multiple failed biometrics attempts (use OS logic on number of attempts)
    And an alternative PIN entry screen is displayed stating that biometrics was not successful
    And stating a PIN is required to enter
    And they enter thier PIN as "369369"
    And they have access to the app


  @T004-Security @AcceptanceTest @normal @Story_146 @Story_93
  Scenario: New User Sets Up PIN
    Given the User has completed on-boarding
    And the User has accepted the Terms and Conditions
    And the User is on the PIN creation screen
    When the User enters the first PIN as "369369"
    And the User re-enters the PIN as "369369"
    And the User selects Create PIN
    And the User selects to use Biometrics
    Then they have access to the app

  @T005-Security @AcceptanceTest @ExceptionTest @normal
  Scenario: New User Sets Up PIN but PINs do not match
    Given the User has skipped on-boarding
    And the User has accepted the Terms and Conditions
    And the User is on the PIN creation screen
    When the User enters the first PIN as "369369"
    And the User re-enters the PIN as "369363"
    And the User selects Create PIN
    Then they are informed that the PINs do not match
    And they select ok on PINs do not match
  # TODO uncomment the below when a solution to entering the pin a second time is solved.
  # And the User re-enters the PIN as "369369"
  # And the User selects Create PIN
  # And the User has successfully created a PIN
  # And they land on the Home screen

  @T006-Security @FunctionalTest @ExceptionTest @normal
  Scenario Outline: New User Sets Up PIN but does not follow conventions
    Given the User has skipped on-boarding
    And the User has accepted the Terms and Conditions
    And the User is on the PIN creation screen
    When the User enters the first PIN as <pin>
    And the User re-enters the PIN as <pin>
    And the User selects Create PIN
    Then they are informed of <pin_error>

    Examples:
      # TODO add more examples
      | pin    | pin_error                                                |
      | 2357   | Your PIN is too short. Please try again.                 |
      | 27463A | Your PIN needs to only contain digits. Please try again. |
    @wip
    Examples:
      | 000000 | Please use only number in your PIN |

  @T00x-Security @AcceptanceTest @ExceptionTest @normal @wip
  Scenario: New User Sets Up PIN but not biometrics and authenticates with PIN
    Given the Holder has setup thier Wallet
    And the Holder has selected to use PIN only to unlock BC Wallet
    And they have closed the app
    When they relaunch the app
    And authenticates with thier PIN as "369369"
    Then they have access to the app

  @T00x-Security @AcceptanceTest @ExceptionTest @normal @wip
  Scenario: New User Sets Up PIN but not biometrics and fails to authenticate with PIN once
    Given the Holder has setup thier Wallet
    And the Holder has selected to use PIN only to unlock BC Wallet
    And they have closed the app
    When they relaunch the app
    And authenticates with thier PIN as "969363"
    Then ?

  @T00x-Security @AcceptanceTest @ExceptionTest @normal @wip
  Scenario: New User Sets Up PIN but not biometrics and fails to authenticate with PIN multiple times
    Given the Holder has setup thier Wallet
    And the Holder has selected to use PIN only to unlock BC Wallet
    And they have closed the app
    When they relaunch the app
    And authenticates with thier PIN as "969363"
    Then ?

  @Story_421 @AcceptanceTest @wip
  Scenario: Holder selects biometrics option in Onbarding with a device that had biometrics setup beforehand
    Given the holder has successfully created their PIN during onboarding
    When the Holder selects "Create PIN"
    Then the Holder is taken to the Biometrics page
    And the option "use device biometrics" is default selected

  @Story_421 @AcceptanceTest @wip
  Scenario: Holder selects biometrics option in Onbarding with a device that didn't have biometrics setup beforehand
    #Scenario: Holder does not have biometrics setup in their wallet
    Given the Holder does not have biometrics setup in their wallet
    When the Holder selects to use biometrics to unlock BC Wallet
    Then a notification pops up stating that they do not have biometrics unlock and to add it in phone settings

  @Story_421 @AcceptanceTest @wip
  #Scenario: Holder has chooses to not use biometrics
  Scenario: Holder chooses to use PIN instead of biometrics
    Given the Holder has selected to use Wallet PIN only to unlock BC Wallet
    When the Holder opens the app
    Then they are prompted to input their wallet PIN

  @T00X-Security @critical @FunctionalTest @Story_421 @wip
  Scenario: Holder chooses biometrics on setup, gets credential, and reopens to biometrics authentication and has access to thier credential

  @T00X-Security @critical @FunctionalTest @ExceptionTest @Story_? @wip
  Scenario: Holder chooses biometrics on setup, gets credential, and reopens to biometrics authentication but fails once, then authenticates and has access to thier credential

  # Below this line has not been decided on and is remaining in the backlog

  @Story_425 @AcceptanceTest @wip
  Scenario: Force PIN entry on app resume if biometrics have changed
    Given the biometrics have changed on the phone
    And biometrics has been enabled in the app
    When the holder attempts to open the app
    Then they are presented with an alternative PIN entry screen that informs them that their biometrics have changed and must enter their wallet PIN

  @Story_425 @AcceptanceTest @wip
  Scenario: Force PIN entry on app resume if biometrics have changed and is successful in PIN entry
    Given the holder has entered the correct PIN after biometrics have changed
    When the holder attempts to open the app
    Then the holder is presented with the basic PIN entry screen

  @Story_422 @AcceptanceTest @wip
  Scenario: Holder enables Biometrics in app but is not enabled on device
    Given Biometrics is not enabled or added on their device
    When the Holder selects to enable Biometrics in BC Wallet
    Then an error notification appears
    And the error notification contains a link to the device's phone settings.
    And a button to dismiss the notification

  @Story_422 @AcceptanceTest @wip
  Scenario: Holder enables Biometrics in app after not being enabled in app
    Given the Holders device has fingerprint or facial data stored within their device security
    When the Holder selects to enable Biometrics in BC Wallet
    Then the holder is prompted enter their wallet PIN
    Then the holder is prompted to confirm their biometrics
    And the toggle button switches to "ON" state when fingerprint or face is verified.

  @Story_422 @AcceptanceTest @wip
  Scenario: Holder enables Biometrics in app
    Given Biometrics is enabled on their device
    When the Holder selects to enable Biometrics in BC Wallet
    Then the holder is prompted to confirm login access by reaffirming their fingerprint or face recognition
    And the toggle button switches to "ON" state when fingerprint or face is verified.

  @Story_425 @ExeptionTest @FunctionalTest @wip
  Scenario: Force PIN entry on app resume if biometrics have changed and is unsuccessful in PIN entry

  @AcceptanceTest @wip
  Scenario: Holder enables Biometrics when onboarding, then disables, then re-enables in app settings

  @AcceptanceTest @wip
  Scenario: Holder leaves Biometrics off when onboarding, then enables, then disables in app settings
