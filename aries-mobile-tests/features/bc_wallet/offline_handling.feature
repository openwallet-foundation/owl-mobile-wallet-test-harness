# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/386
# Stories Below are not finalized yet
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/414
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/413
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/392
@OfflineHandling @bc_wallet
Feature: Wallet Offline Handling
  In order to have a seemless experience in the wallet and make any corrections to my device that could hinder my wallet experience
  As user of BC Wallet
  I want to to know when I loose internet connectivity


  # This test will remain flacky until we are out of the crawl stage and the test code is refined to properly
  # use swipe to toggle WiFi on control center on iOS. 
  # Android in SL has issues when coming back into a closed app, biometrics at times does not display.
  @T001-OfflineHandling @critical @AcceptanceTest @Story_386 @crawl
  Scenario: Holder opens BC Wallet while mobile phone is offline
    Given the Holder has setup thier Wallet
    And the Holder has selected to use biometrics to unlock BC Wallet
    And they have closed the app
    And the mobile phone does not have an internet connection
    When the holder opens BC Wallet
    #And authenticates with thier biometrics
    #And initialization ends (failing silently)
    Then they are presented with a dismissible "no internet connection" toast notification


  @T002-OfflineHandling @critical @AcceptanceTest @Story_386 @crawl
  Scenario Outline: BC Wallet does not detect internet connection while in use
    Given the holder is <using the app>
    When the mobile phone does not have an internet connection
    Then they are presented with a dismissible "no internet connection" toast notification

    Examples:
      | using the app        |
      | Onboarding           |
      | PIN Setup            |
      | Receiving Credential |
      | Presenting Proof     |


  @T003-OfflineHandling @critical @AcceptanceTest @Story_386 @crawl @wip
  Scenario Outline: BC Wallet is offline and returns back online
    Given the holder is <using the app>
    And the mobile phone does not have an internet connection
    When BC Wallet suddenly goes back online
    Then they are presented with a temporary "Your internet connection is back" toast notification
    And the toast notification goes away after "5" seconds

    Examples:
      | using the app        |
      | Onboarding           |
      | PIN Setup            |
      | Receiving Credential |
      | Presenting Proof     |


  @T004-OfflineHandling @critical @AcceptanceTest @Story_386 @crawl @wip
  Scenario Outline: BC Wallet is offline and holder changes screens optional
    Given the Holder has setup thier Wallet
    And the mobile phone does not have an internet connection
    When the holder navigates from one <screen> to <another screen>
    Then they are presented with a dismissible "no internet connection" toast notification

    Examples:
      | screen               | another screen |
      | Onboarding           | PIN Setup      |
      | PIN Entry            | Home           |
      | Home                 | Settings       |
      | Receiving Credential | Home           |
      | Presenting Proof     | Home           |



  # SCENARIOS BELOW ARE NOT FINALIZED YET.
  @Story_414 @wip
  Scenario: BC Wallet is offline during a credential offer
    Given the BC Wallet is offline
    And the Holder is completing a credential offer
    When the Holder selects "accept" (the accept button is not disabled)
    Then the Holder is presented with a modal that states "You'll receive your credential in your wallet when you're back online"
    And a "okay" button

  @Story_413 @wip
  Scenario: BC Wallet is offline during a credential offer
    Given the holder has accepted a credential offer while offline
    When BC Wallet has gone back online
    And the credential offer flow is completed in the background
    Then a notification appears in the notification section of the Home stating: "New credential added to your wallet"

  @Story_392 @wip @walk
  Scenario: The Holder uses the wallet while BC Wallet is offline
    Given the BC Wallet is offline
    When the Holder selects "Scan"
    Then they are presented with a dismissible notification modal

  @Story_392 @wip @walk
  Scenario: The Holder uses the wallet while BC Wallet is offline
    Given the BC Wallet is offline
    And the the Holder is in proof request screen
    When the Holder selects "Send"
    Then they are presented with a dismissible notification modal

  @Story_392 @wip @walk
  Scenario: The Holder uses the wallet while BC Wallet is offline
    Given the BC Wallet is offline
    When the Holder selects a contacts chat button (speech bubble)
    Then they move to the chat of the contact
    And an offline error notification appears
    And the send button is disabled

  @Story_392 @wip @walk
  Scenario: The Holder uses the wallet while BC Wallet is offline
    Given the BC Wallet is offline
    And the the Holder is in credential offer screen
    When the Holder selects "Accept offer"
    Then they are presented with a dismissible notification modal that states "You're unable to access services using BC Wallet or receive credentials until you're back online. Please check you internet connection."

  @Story_392 @wip @walk
  Scenario: The Holder uses the wallet while BC Wallet is offline
    Given the holder waiting for a transaction to complete
    When BC Wallet goes offline
    Then they are presented with an error notification stating that they have "no internet connection"

  @Story_392 @wip @run
  Scenario: BC Wallet is offline during a credential offer
    Given the BC Wallet is offline
    And the Holder is completing a credential offer
    When the Holder selects "accept" (the accept button is not disabled)
    Then the Holder is presented with a modal that states "You'll receive your credential in your wallet when you're back online"
    And a "okay" button

  @Story_392 @wip @run
  Scenario: BC Wallet is offline during an acceptance of a credential offer
    Given the holder has accepted a credential offer while offline
    When BC Wallet has gone back online
    And the credential offer flow is completed in the background
    Then a notification appears in the notification section of the Home stating: "New credential added to your wallet"