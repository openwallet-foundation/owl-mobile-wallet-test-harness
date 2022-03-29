"""
Factory class to create agent interface objects 
given the agent type passed in.
"""
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_factory.verifier_agent_interface import VerifierAgentInterface
from agent_factory.aath.aath_issuer_agent_interface import AATHIssuerAgentInterface
from agent_factory.aath.aath_verifier_agent_interface import AATHVerifierAgentInterface


class AgentInterfaceFactory():
    
    issuer_agent_type_interface_dict = {
        "AATH": AATHIssuerAgentInterface
    }
    verifier_agent_type_interface_dict = {
        "AATH": AATHVerifierAgentInterface
    }
    
    def create_issuer_agent_interface(self, agent_type, agent_endpoint) -> IssuerAgentInterface:
        """create an issuer agent interface object of the type given"""
        return self.issuer_agent_type_interface_dict[agent_type](agent_endpoint)

    def create_verifier_agent_interface(self, agent_type, agent_endpoint) -> VerifierAgentInterface:
        """create a verifier agent interface object of the type given"""
        return self.verifier_agent_type_interface_dict[agent_type](agent_endpoint)