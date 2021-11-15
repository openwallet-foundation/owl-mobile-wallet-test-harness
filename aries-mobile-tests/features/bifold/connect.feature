Feature: Connect to an Issuer

   @T001-Connect
   Scenario: Connect to an Issuer based on a QR code
      Given the terms of service has been accepted
      And a PIN has been set up
      When the wallet user scans the QR code sent by the issuer
      And accepts the connection
      Then there is a connection between Issuer and wallet user
