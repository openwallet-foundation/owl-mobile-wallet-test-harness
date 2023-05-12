# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/76
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/82
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/231
@Connect @bc_wallet @Story_76
Feature: Connections


   @T001-Connect @wip @critical @AcceptanceTest
   Scenario: Scan QR code to recieve a credential offer
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      When the Holder scans the QR code sent by the "issuer"
      And the Holder is taken to the Connecting Screen/modal
      And the Connecting completes successfully
      Then there is a connection between "issuer" and Holder

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


   @T005.1-Connect @RemoveContact @normal @AcceptanceTest @Story_231
   Scenario Outline: Remove an Issuer contact where no credentials are issued from that contact
      Given the holder is connected to an Issuer
      And there are <no_credentials> issued by this Contact in the holders wallet
      When the holder Removes this Contact
      And the holder reviews more details on removing Contacts
         | details                                                            |
         | To add credentials, the issuing organization needs to be a contact |
      And the holder confirms to Remove this Contact
      Then the holder is taken to the Contact list
      And the holder is informed that the Contact has been removed
      And the Contact is removed from the wallet

      Examples:
         | no_credentials       |
         | Offered and Rejected |
   #| Issued and Deleted         |
   #| Issued Revoked and Deleted |


   @T005.2-Connect @RemoveContact @normal @AcceptanceTest @Story_231 @wip
   Scenario Outline: Remove a Verifier contact after a proof presentation
      Given the holder is connected to a Verifier
      And there has been a <proof> by this verifier
      And the holder is viewing that Contacts details
      When the holder Removes this Contact
      And the holder reviews more details on removing Contacts
      And the holder confirms to Remove this Contact
      Then the holder is taken to the Contact list
      And the holder is informed that the Contact has been removed
      And the Contact is removed from the wallet

      Examples:
         | proof      |
         | successful |
         | rejected   |


   @T005.3-Connect @RemoveContact @normal @AcceptanceTest @Story_231 @wip
   Scenario: Remove a contact where 1 or more credentials are issued from that contact and Cancels by going to Credentials
      Given the holder is connected to an Issuer
      And the holder has credentials
         | credential                | revocable | issuer_agent_type | credential_name |
         | cred_data_drivers_license | True      | AATHIssuer        | Drivers License |
         | cred_data_photo_id        | True      | AATHIssuer        | Photo Id        |
      And the holder is viewing that Contacts details
      When the holder Removes this Contact
      Then the holder is informed that it can't be removed because there are credentials issued by this contact in their wallet
      And the holder goes to credentials
      And the holder is taken to the Credential List
      And the Contact is not removed from the wallet


   @T005.4-Connect @RemoveContact @normal @AcceptanceTest @Story_231 @wip
   Scenario: Remove a contact where 1 or more credentials are issued from that contact and Cancels
      Given the holder is connected to an Issuer
      And the holder has credentials
         | credential                | revocable | issuer_agent_type | credential_name |
         | cred_data_drivers_license | True      | AATHIssuer        | Drivers License |
         | cred_data_photo_id        | True      | AATHIssuer        | Photo Id        |
      And the holder is viewing that Contacts details
      When the holder Removes this Contact
      Then the holder is informed that it can't be removed because there are credentials issued by this contact in their wallet
      And the holder Cancels
      And the holder is taken to Contacts details
      And the Contact is not removed form the wallet

   @T005.5-Connect @RemoveContact @normal @NegativeTest @Story_231 @wip
   Scenario: Remove a contact where 1 or more credentials are issued and revoked from that contact and Cancels
      Given the holder is connected to an Issuer
      And the holder has credentials
         | credential                | revocable | issuer_agent_type | credential_name |
         | cred_data_drivers_license | True      | AATHIssuer        | Drivers License |
      And the credential has been revoked by the issuer
      And the holder is viewing that Contacts details
      When the holder Removes this Contact
      Then the holder is informed that it can't be removed because there are credentials issued by this contact in their wallet
      And the holder Cancels
      And the holder is taken to Contacts details
      And the Contact is not removed form the wallet

   @T005.6-Connect @RemoveContact @minor @AcceptanceTest @Story_231 @wip
   Scenario Outline: Remove an Issuer contact then try to issue a credential based on that connection
      Given the holder is connected to an Issuer
      And there are <no credentials> issued by this Contact in the holder's wallet
      And the holder is viewing that Contacts details
      When the holder Removes this Contact from the wallet
      And the issuer attempts to issue a credential to the holder with the same connection
      Then the issuer is informed that the holder and issuer are not connected?
      And the issuer will be informed that the connection is invalid?

      Examples:
         | no credentials     |
         | Issued and Deleted |

   @T005.7-Connect @RemoveContact @minor @ExceptionTest @Story_231 @wip
   Scenario: Remove a Verifier contact then try to request a proof based on that connection

   @T005.8-Connect @RemoveContact @minor @ExceptionTest @Story_231 @wip
   Scenario: Remove contact after a Credential Offer but before Accepting

   @T005.9-Connect @RemoveContact @minor @ExceptionTest @Story_231 @wip
   Scenario: Remove contact after a Proof Request but before Sending

   # Messaging/Chat currently not implemented/turned off in BC Wallet
   @T005.10-Connect @RemoveContact @trivial @ExceptionTest @Story_231 @wip
   Scenario: Messaging/Chat after contact removal