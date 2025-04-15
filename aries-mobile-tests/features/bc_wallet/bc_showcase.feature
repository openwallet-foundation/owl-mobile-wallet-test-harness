#TODO: Only features are written, no steps or pages
@BCShowcase
Feature: BC Showcase
   In order to easily show the capabilities of BC Wallet and ensure those services are working
   As a BC Wallet Stakeholder
   I want to be able to run nightly tests on the BC Showcase with BC Wallet


   @T001-BCShowcase @critical @AcceptanceTest
   Scenario: BC Showcase Student gets access to a store discount
      Given an existing Student wallet user
         | pin    | biometrics |
         | 369369 | off        |
      When the Student has credentials
         | credential | revocable | issuer_agent_type             | credential_name |
         | N/A        | False     | BCShowcaseBestBCCollegeIssuer | Student Card    |
      And the Student has a proof request
         | verifier_agent_type             | proof_request       |
         | BCShowcaseBestBCCollegeVerifier | Cool Clothes Online |
      And they select Share
      Then they have Access
         | proof_result |
         | Discount     |

   @T002-BCShowcase @critical @AcceptanceTest
   Scenario: BC Showcase Student gets access to a book a room
      Given an existing Student wallet user
         | pin    | biometrics |
         | 369369 | off        |
      When the Student has credentials
         | credential | revocable | issuer_agent_type             | credential_name |
         | N/A        | False     | BCShowcaseBestBCCollegeIssuer | Student Card    |
      And the Student has a proof request
         | verifier_agent_type             | proof_request  |
         | BCShowcaseBestBCCollegeVerifier | BestBC College |
      And they select Share
      Then they have Access
         | proof_result |
         | Room Booked  |


   @T003-BCShowcase @critical @AcceptanceTest @wip
   Scenario: BC Showcase Lawyer gets access to court services
      Given an existing Lawyer wallet user
         | pin    | biometrics |
         | 369369 | off        |
      When the Lawyer has credentials
         | credential | revocable | issuer_agent_type    | credential_name         |
         | N/A        | False     | BCShowcaseLSBCIssuer | LSBC Member Card:Person |
      And the Lawyer has a proof request
         | verifier_agent_type                   | proof_request        |
         | BCShowcaseCourtServicesBranchVerifier | Member Card & Person |
      And they select Share
      Then they have Access
         | proof_result   |
         | Court Services |