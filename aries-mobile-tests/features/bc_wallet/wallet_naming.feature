# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/1200
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/1148
@WalletNaming @bc_wallet
Feature: Wallet Naming
  In order for contacts to be easily distinguished
  As a wallet user who connects with other people and organizations
  I want to be able to set how I'm represented in other people's wallets & set other contacts' names


  @T001-WalletNaming @AcceptanceTest @Story_1200 @normal @CanRunOnSLVirtualDevice
  Scenario Outline: Wallet user updates and saves thier wallet name
    Given an existing wallet user
      | pin    | biometrics |
      | 369369 | off        |
    And the wallet user is in <user_state>
    When the user changes thier wallet name
      | wallet_name                                        |
      | This is my wallet name at 50 Characters @123456789 |
    And saves the wallet name change
    Then the name of the wallet is changed everywhere it is presented
      | wallet_name_location |
      | the menu             |
      | Scan my QR code      |
    #| a connection's contact list |
    #| a connection's messaging    |

    Examples:
      | user_state |
      | the menu   |
      | Scan my QR code |


  @T002-WalletNaming @AcceptanceTest @Story_1200 @normal @CanRunOnSLVirtualDevice
  Scenario Outline: Wallet user cancels the update of thier wallet name
    Given an existing wallet user
      | pin    | biometrics |
      | 369369 | off        |
    And the wallet user is in <user_state>
    When the user changes thier wallet name
      | wallet_name                                        |
      | This is my wallet name at 50 Characters @123456789 |
    And cancels the wallet name change
    Then the name of the wallet is unchanged everywhere it is presented
      | wallet_name_location |
      | the menu             |
      | Scan my QR code      |

    Examples:
      | user_state |
      | the menu   |
      | Scan my QR code |

  @T002.1-WalletNaming @FunctionalTest @Story_1200 @minor @CanRunOnSLVirtualDevice
  Scenario Outline: Wallet user updates and saves thier wallet name, then changes back to original name
    Given an existing wallet user
      | pin    | biometrics |
      | 369369 | off        |
    And the wallet user is in the menu
    When the user changes thier wallet name
      | wallet_name                                        |
      | This is my wallet name at 50 Characters @123456789 |
    And saves the wallet name change
    And changes the wallet name back to the original name
    Then the name of the wallet is unchanged everywhere it is presented
      | wallet_name_location |
      | the menu             |
      | Scan my QR code      |
    #| a connection's contact list |
    #| a connection's messaging    |

    Examples:
      | user_state |
      | the menu   |
      | Scan my QR code |

  @T003-WalletNaming @AcceptanceTest @Story_1148 @normal @wip
  Scenario: New Wallet User updates thier wallet name during onboarding
    Given the holder has just installed BC Wallet
    And is going through the onboarding process
    When the holder continues from the "Lock biometrics screen"
    Then they are presented with the option to name their wallet
    And the default name of the wallet is "My Wallet"
    And they are presented with the option to tap "not now" to complete this step later


  @T004-WalletNaming @AcceptanceTest @Story_1148 @normal @wip
  Scenario: New Wallet User Chooses not to update thier wallet name during onboarding


  @T005-WalletNaming @AcceptanceTest @Story_1148 @normal @CanRunOnSLVirtualDevice
  Scenario: Wallet User does not follow conventions when naming thier wallet
    Given an existing wallet user
      | pin    | biometrics |
      | 369369 | off        |
    And the wallet user is in the menu
    When the user changes thier wallet name not following conventions
    Then the user will be informed on the wallet name conventions
      | wallet_name                                          | wallet_name_error          |
      |                                                      | Wallet name can't be empty |
      | over 50 characters is not allowed in the wallet 1234 | Character count exceeded   |



  @T006-WalletNaming @AcceptanceTest @Story_1148 @minor @CanRunOnSLVirtualDevice
  Scenario: Wallet User follows conventions when naming thier wallet but is a weirdo
    Given an existing wallet user
      | pin    | biometrics |
      | 369369 | off        |
    And the wallet user is in the menu
    When the user changes thier wallet name following conventions
    Then the name of the wallet is successfully changed
      | wallet_name                                        |
      | *                                                  |
      | http://www.iamverystrangewhennamingwallets.com     |
      | @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
      | SELECT * FROM Users                                |
      | rm -rf *                                           |
      | /0                                                 |
      | 0                                                  |
      | break                                              |
      | throw                                              |
      | finally                                            |
      | const lv_conf_result = showConfirmPopup("inject"); |
      | alert("Code Injection Test");                      |
      | <script>alert("Code Injection Test");</script>     |
      | import os; os.system("echo Code Injection Test")   |
      | Fuck                                               |
      | name_😀                                            |

  # This will remain on hold until an approach to testing with multiple wallets concurrently in AMTH is solidified.
  @T007-WalletNaming @AcceptanceTest @Story_1148 @minor @wip
  Scenario: Wallet weirdo User follows conventions when naming thier wallet then connects with others