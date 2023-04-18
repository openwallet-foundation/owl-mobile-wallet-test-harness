@CredentialOffer @qc_wallet @Story_81
Feature: Offer a Credential
   In order have confidence and control of my wallet
   As a holder
   I want to be able to review, accept, and decline a credential offer

  @T003.x-CredentialOffer @critical @AcceptanceTest
   Scenario: Holder declines the credential offer recieved
      Given the User has skipped on-boarding
      And the User has accepted the Terms and Conditions
      And a PIN has been set up with "369369"
      And the Holder has selected to use biometrics to unlock BC Wallet
      And a connection has been successfully made
      And the user has a credential offer
      When they select Decline the credential
      Then they are brought to the confirm decline page
      And they select Yes, decline this credential
      When they select Done
      Then they are brought Home
      # Then they are brought to the list of credentials
      # And a temporary notification will appear that informs the holder of the declined action
      # And the credential declined is not in the list
      # Then the holder will be taken to the credential list page
      # And a temporary notification will appear that informs the holder of the declined action
      #
