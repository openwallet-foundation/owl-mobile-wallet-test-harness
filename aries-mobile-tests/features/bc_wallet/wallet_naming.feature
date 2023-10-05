# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/1200
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/1148
@WalletNaming @bc_wallet
Feature: Wallet Naming
  In order for contacts to be easily distinguished
  As a wallet user who connects with other people and organizations
  I want to be able to set how I'm represented in other people's wallets & set other contacts' names


  @T001-WalletNaming @AcceptanceTest @Story_1200 @normal
  Scenario Outline: Wallet user updates and saves thier wallet name
    Given an existing wallet user
      | pin    | biometrics |
      | 369369 | off        |
    And the wallet user is in <user_state>
    When the user changes thier wallet name
      | wallet_name                                         |
      | This is my wallet name at 50 Characters 0123456789@ |
    And saves the wallet name change
    Then the name of the wallet is changed everywhere it is presented
      | wallet_name_location        |
      | the menu                    |
      | Scan my QR code             |
      | a connection's contact list |
      | a connection's messaging    |

    Examples:
      | user_state      |
      #| the menu        |
      | Scan my QR code |


  @T002-WalletNaming @AcceptanceTest @Story_1200 @normal @wip
  Scenario Outline: Wallet user cancels the update of thier wallet name
    Given an existing wallet user
    And the wallet user <user_state>
    When the user changes thier wallet name
    And cancels the wallet name change
    Then the name of the wallet is changed everywhere it is presented
      | wallet_name_location  |
      | is in the menu        |
      | is in Scan my QR code |

    Examples:
      | user_state            |
      | is in the menu        |
      | is in Scan my QR code |


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


  @T005-WalletNaming @AcceptanceTest @Story_1148 @normal @wip
  Scenario: Wallet User does not follow conventions when naming thier wallet
      | wallet_name                                     | wallet_name_error          |
      | empty                                           | Wallet name can't be empty |
      | over 50 characters is not allowed in the wallet | Character count exceeded   |


  @T005-WalletNaming @AcceptanceTest @Story_1148 @minor @wip
  Scenario: Wallet User follows conventions when naming thier wallet but is a weirdo
      | wallet_name                                            |
      | *                                                      |
      | http://www.iamverystrangewhennamingwallets.com         |
      | @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ |
      | sql injection                                          |
      | rm -rf *                                               |
      | / 0                                                    |
      | 0                                                      |
      | react native reserved words                            |
      | javascript reserved words                              |
      | python reserved words                                  |
      | react native code injection                            |
      | javascript code injection                              |
      | python code injection                                  |
      | obcenities                                             |
      | calls to acapy or afj api to get holder info?          |
      | emoji                                                  |



Default wallet name: "My Wallet - "
Acceptable Characters: Any character (including \, ")
Minimum Characters: 1
Maximum character count: 50
