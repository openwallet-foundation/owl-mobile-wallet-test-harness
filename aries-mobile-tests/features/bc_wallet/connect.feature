# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/76
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/82
@Connect @bc_wallet @Story_76
Feature: Connect to an Issuer/Scan QR Code for Credential


   @T001-Connect @wip @critical @AcceptanceTest
   Scenario: Scan QR code to recieve a credential offer
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      When the Holder scans the QR code sent by the issuer
      And the Holder is taken to the Connecting Screen/modal
      And the Connecting completes successfully
      Then there is a connection between Issuer and Holder

   @T002-Connect @wip @normal @AcceptanceTest
   Scenario: Scan QR code to recieve a credential offer but exits scanning

   @T003-Connect @wip @minor @FunctionalTest
   Scenario: Scan QR code with flash on to recieve a credential offer

   @T004-Connect @Story_82 @ExceptionTest @wip
   Scenario: Holder is waiting for Connection (failure)
      Error modal wireframes
      Given the holder has scanned a QR code invitation
      And waiting for connection to be established
      When the connection fails to be established
      Then a temporary error notification (toast) is displayed with an error message
      And go back to the home screen
   #Alternative
   @wip
   Scenario: Holder is waiting for Connection (failure)
      Given the holder has scanned a QR code invitation
      And waiting for connection to be established
      When the connection fails to be established
      Then a full screen modal is displayed with an error message
      And a button to back to the home screen
   #Alternative
   @wip
   Scenario Outline: Holder is waiting for Connection (failure)
      Given the holder has a valid QR code invitation (is it true that the QR code is valid in this case?)
      When they scan the QR code invitation
      #(I don't think we need (but you can) state they are waiting, that is a side effect of the scan)
      And the connection fails to be established for <reason>
      Then a temporary error notification (toast) is displayed <error message> (are there specific errors for the different reasons?)
      And they are taken back to the home screen (I'd reframe this to taken, so it is not misinterpreted that the user manually goes back to the home screen)

      Examples:
         | reason                                     | error message                |
         | timeout?                                   | this is taking too long man! |
         | no internet connectivity at point of scan? | No internet                  |
         | what other reasons?                        | I don't know                 |

   #I think this is obsolete
   @Story_82 @wip
   Scenario: Holder is waiting for Connection (success)
      Given the holder has scanned a QR code invitation
      And waiting for connection to be established
      When the connection is established
      Then the screen automatically takes the Holder to the offer screen