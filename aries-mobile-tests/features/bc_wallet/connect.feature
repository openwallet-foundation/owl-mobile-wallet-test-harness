# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/76
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/bcgov/bc-wallet-mobile/82
# https://app.zenhub.com/workspaces/bc-wallet-6148e7423fe04b001444e2bd/issues/gh/bcgov/bc-wallet-mobile/231
@Connect @bc_wallet @Story_76
Feature: Connections

   @T001-Connect @critical @AcceptanceTest
   Scenario: Scan QR code to establish a connection
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      When the Holder scans the QR code sent by the "issuer"
      And the Holder is taken to the Connecting Screen/modal
      And the Connecting completes successfully
      Then there is a connection between "issuer" and Holder
   
   @T002-Connect @RemoveContact @normal @AcceptanceTest @Story_231
   Scenario: Remove an Issuer contact where no credentials are issued from that contact
      Given the User has completed on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has opted out of biometrics to unlock BC Wallet
      When the Holder scans the QR code sent by the "issuer"
      And the Holder is taken to the Connecting Screen/modal
      And the Connecting completes successfully
      Then there is a connection between "issuer" and Holder
      When the holder Removes this Contact
      When the holder confirms to Remove this Contact
      Then the holder is brought back to the home screen

   # @T003-Connect @wip @minor @FunctionalTest
   # Scenario: Scan QR code with flash on to recieve a credential offer

   # NOT WORKING
   # @T004-Connect @Story_82 @ExceptionTest @wip
   # Scenario: Holder is waiting for Connection (failure)


   # @T005.2-Connect @RemoveContact @normal @AcceptanceTest @Story_231 @wip
   # Scenario Outline: Remove a Verifier contact after a proof presentation
   #    Given the holder is connected to a Verifier
   #    And there has been a <proof> by this verifier
   #    And the holder is viewing that Contacts details
   #    When the holder Removes this Contact
   #    And the holder reviews more details on removing Contacts
   #    And the holder confirms to Remove this Contact
   #    Then the holder is taken to the Contact list
   #    And the holder is informed that the Contact has been removed
   #    And the Contact is removed from the wallet

   #    Examples:
   #       | proof      |
   #       | successful |
   #       | rejected   |


   # @T005.3-Connect @RemoveContact @normal @AcceptanceTest @Story_231 @wip
   # Scenario: Remove a contact where 1 or more credentials are issued from that contact and Cancels by going to Credentials
   #    Given the holder is connected to an Issuer
   #    And the holder has credentials
   #       | credential                | revocable | issuer_agent_type | credential_name |
   #       | cred_data_drivers_license | True      | TractionIssuer        | Drivers License |
   #       | cred_data_photo_id        | True      | TractionIssuer        | Photo Id        |
   #    And the holder is viewing that Contacts details
   #    When the holder Removes this Contact
   #    Then the holder is informed that it can't be removed because there are credentials issued by this contact in their wallet
   #    And the holder goes to credentials
   #    And the holder is taken to the Credential List
   #    And the Contact is not removed from the wallet


   # @T005.4-Connect @RemoveContact @normal @AcceptanceTest @Story_231 @wip
   # Scenario: Remove a contact where 1 or more credentials are issued from that contact and Cancels
   #    Given the holder is connected to an Issuer
   #    And the holder has credentials
   #       | credential                | revocable | issuer_agent_type | credential_name |
   #       | cred_data_drivers_license | True      | TractionIssuer        | Drivers License |
   #       | cred_data_photo_id        | True      | TractionIssuer        | Photo Id        |
   #    And the holder is viewing that Contacts details
   #    When the holder Removes this Contact
   #    Then the holder is informed that it can't be removed because there are credentials issued by this contact in their wallet
   #    And the holder Cancels
   #    And the holder is taken to Contacts details
   #    And the Contact is not removed form the wallet

   # @T005.5-Connect @RemoveContact @normal @NegativeTest @Story_231 @wip
   # Scenario: Remove a contact where 1 or more credentials are issued and revoked from that contact and Cancels
   #    Given the holder is connected to an Issuer
   #    And the holder has credentials
   #       | credential                | revocable | issuer_agent_type | credential_name |
   #       | cred_data_drivers_license | True      | TractionIssuer        | Drivers License |
   #    And the credential has been revoked by the issuer
   #    And the holder is viewing that Contacts details
   #    When the holder Removes this Contact
   #    Then the holder is informed that it can't be removed because there are credentials issued by this contact in their wallet
   #    And the holder Cancels
   #    And the holder is taken to Contacts details
   #    And the Contact is not removed form the wallet

   # @T005.6-Connect @RemoveContact @minor @AcceptanceTest @Story_231 @wip
   # Scenario Outline: Remove an Issuer contact then try to issue a credential based on that connection
   #    Given the holder is connected to an Issuer
   #    And there are <no credentials> issued by this Contact in the holder's wallet
   #    And the holder is viewing that Contacts details
   #    When the holder Removes this Contact from the wallet
   #    And the issuer attempts to issue a credential to the holder with the same connection
   #    Then the issuer is informed that the holder and issuer are not connected?
   #    And the issuer will be informed that the connection is invalid?

   #    Examples:
   #       | no credentials     |
   #       | Issued and Deleted |

   # @T005.7-Connect @RemoveContact @minor @ExceptionTest @Story_231 @wip
   # Scenario: Remove a Verifier contact then try to request a proof based on that connection

   # @T005.8-Connect @RemoveContact @minor @ExceptionTest @Story_231 @wip
   # Scenario: Remove contact after a Credential Offer but before Accepting

   # @T005.9-Connect @RemoveContact @minor @ExceptionTest @Story_231 @wip
   # Scenario: Remove contact after a Proof Request but before Sending

   # # Messaging/Chat currently not implemented/turned off in BC Wallet
   # @T005.10-Connect @RemoveContact @trivial @ExceptionTest @Story_231 @wip
   # Scenario: Messaging/Chat after contact removal