@BCShowcase @bc_wallet
Feature: BC Showcase
   In order to easily show the capabilities of BC Wallet and ensure those services are working
   As a BC Wallet Stakeholder
   I want to be able to run nightly tests on the BC Showcase with BC Wallet


   @T001-BCShowcase @critical @AcceptanceTest
   Scenario Outline: BC Showcase Student gets access to a store discount
      Given a <user> wallet user
         | pin    | biometrics |
         | 369369 | off        |

      When the <user> has a <credentials> from <issuer_agent_type>
      When the Student has credentials
         | credential | revocable | issuer_agent_type             | credential_name |
         | N/A        | False     | BCShowcaseBestBCCollegeIssuer | Student Card    |

      And the <user> has a proof request of <proof_request> from <verifier_agent_type>
      And the Student has a proof request
         | verifier_agent_type             | proof_request |
         | BCShowcaseBestBCCollegeVerifier | Student Card  |

      And they select Share

      Then they have <proof_result>
      Then they have Access
         | proof_result |
         | Room Booked  |

      Examples:
         | user    | issuer_agent_type             | credentials             | verifier_agent_type                   | proof_request        | proof_result   |
         | Student | BCShowcaseBestBCCollegeIssuer | Student Card            | BCShowcaseBestBCCollegeVerifier       | Student Card         | Room Booked    |
         | Student | BCShowcaseBestBCCollegeIssuer | Student Card            | BCShowcaseCoolClothesOnlineVerifier   | Student Card         | Discount       |
         | Lawyer  | BCShowcaseLSBCIssuer          | LSBC Member Card:Person | BCShowcaseCourtServicesBranchVerifier | Member Card & Person | Court Services |

BCShowcaseServiceBCIssuer Person