@HelpCenterQC @qc_wallet @normal
Feature: Help Center

@T001-helpCenter @AcceptanceTest 
Scenario: User open help center page
Given the Holder has setup thier Wallet and land on the Home screen
When the Holder opens more options page
And the Holder open help center page
Then Help Center page is displayed 

@T002-helpCenter @AcceptanceTest
Scenario: User open what is a PIN info page in the help center module
Given the Holder is on the help center page
When the Holder click on PIN
Then What is a PIN info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed 

@T003-helpCenter @AcceptanceTest 
Scenario: User open what is Biometrics info page in the help center module
Given the Holder is on the help center page
When the Holder click on Biometrics
Then what is Biometrics info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed 

@T004-helpCenter @AcceptanceTest
Scenario: User open what is a history info page in the help center module
Given the Holder is on the help center page
When the Holder click on activities
Then what is a history info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed 

@T005-helpCenter @AcceptanceTest
Scenario: User open the what is PNG info page in the help center module
Given the Holder is on the help center page
When the Holder click on PNG
Then what is png info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed 

@T006-helpCenter @AcceptanceTest
Scenario: User open receive presentation request info page in the help center module
Given the Holder is on the help center page
When the Holder click on Receive presentation request
Then Receive a presentation request info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed

@T007-helpCenter @AcceptanceTest
Scenario: User open receive a certificate offer info page in the help center module
Given the Holder is on the help center page
When the Holder click on Receive a Certificate Offer
Then receive a certificate offer info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed

@T008-helpCenter @AcceptanceTest
Scenario: User open delete a certificate info page in the help center module
Given the Holder is on the help center page
When the Holder click on Delete a certificate
Then delete a certificate info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed

@T009-helpCenter @AcceptanceTest
Scenario: User open scan a QR code info page in the help center module
Given the Holder is on the help center page
When the Holder click on Scan a QR code
Then scan a QR code info page is displayed
When the Holder click on return to Help Center button
Then Help Center page is displayed