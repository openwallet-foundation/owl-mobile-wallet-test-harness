# -----------------------------------------------------------
# Behave Step Definitions for the Sample test
# 
# -----------------------------------------------------------

from behave import given, when, then
import json

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
# import Page Objects needed
from pageobjects.wikipediahome import WikipediaHomePage

# Instantiate the page objects needed
# Can I pass the context here on instantiation or should we do it in the steps? 
# We could put a page factory somewhere that instantiates all pages for a given app. 
iWikipediaHomePage = WikipediaHomePage()

@given('a React Native app in the Device Cloud')
def step_impl(context):
    # Is there anything to do here to make sure the app is in the device cloud? 
    # Should the manage script put the app in teh cloud or can a step like this do it?
    pass

@given('an aries agent is running with a controller with a web service API')
def step_impl(context):
    # Maybe ping the service at this point? 
    pass

@when('the test sends an event to the app')
def step_impl(context):
    # call the page object for the app to do some event
    iWikipediaHomePage.search(context,"tiger")
    #assert True

@when('can retrieve screen contents')
def step_impl(context):
    # call the page object for the app to get some information from the screen
    elems = iWikipediaHomePage.get_search_results(context)
    assert len(elems) > 0, "results not populated"
    for elem in elems:
        print(elem.text)
        if "Tiger" in elem.text:
            assert True

@when('can call the agent web service api')
def step_impl(context):
    # call some web service online pretending it is the agent controller web service
    (resp_status, resp_text) = agent_controller_GET("http://acme_agent:9022/", "connections")
    #(resp_status, resp_text) = agent_controller_POST("http://acme_agent:9022/", "connections", operation="create-invitation", data="{}")
    #(resp_status, resp_text) = agent_controller_POST("agent_url" + "/agent/command/", "connection", operation="create-invitation")
    assert resp_status == 200, f'resp_status {resp_status} is not 200; {resp_text}'

@then('we have a viable test framework')
def step_impl(context):
    # nothing to do here
    pass
    
