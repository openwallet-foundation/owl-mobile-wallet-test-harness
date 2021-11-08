Feature: Sample test specification

   @T001-Sample
   Scenario: Sample scenario to call the app in the device cloud and call the agent controller
      Given a React Native app in the Device Cloud
      And an aries agent is running with a controller with a web service API
      When the test sends an event to the app
      And can retrieve screen contents
      And can call the agent web service api
      Then we have a viable test framework
