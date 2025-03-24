"""
Factory class to create agent interface objects 
given the agent type passed in.
"""
from agent_factory.bc_showcase.bc_showcase_issuer_agent_interface import BCShowcaseIssuerAgentInterface
from agent_factory.bc_showcase.bc_showcase_verifier_agent_interface import BCShowcaseVerifierAgentInterface
from agent_factory.issuer_agent_interface import IssuerAgentInterface
from agent_factory.verifier_agent_interface import VerifierAgentInterface
from agent_factory.aath.aath_issuer_agent_interface import AATHIssuerAgentInterface
from agent_factory.aath.aath_verifier_agent_interface import AATHVerifierAgentInterface
from agent_factory.candy_uvp.candy_uvp_issuer_agent_interface import CANdy_UVP_IssuerAgentInterface
from agent_factory.bc_person_showcase.bc_person_showcase_verifier_agent_interface import BCPersonShowcaseVerifierAgentInterface
from agent_factory.bc_vp.bc_vp_issuer_agent_interface import BC_VP_IssuerAgentInterface
from agent_factory.traction.traction_issuer_agent_interface import TractionIssuerAgentInterface
from agent_factory.traction.traction_verifier_agent_interface import TractionVerifierAgentInterface

class AgentInterfaceFactory():
    
    issuer_agent_type_interface_dict = {
        "AATH": AATHIssuerAgentInterface,
        "CANdy_UVP": CANdy_UVP_IssuerAgentInterface,
        "BC_VP": BC_VP_IssuerAgentInterface,
        "BCShowcaseIssuer": BCShowcaseIssuerAgentInterface,
        "Traction": TractionIssuerAgentInterface
    }
    verifier_agent_type_interface_dict = {
        "AATH": AATHVerifierAgentInterface,
        "BC_Person_Showcase": BCPersonShowcaseVerifierAgentInterface,
        "BCShowcaseVerifier": BCShowcaseVerifierAgentInterface,
        "Traction": TractionVerifierAgentInterface
    }
    
    def create_issuer_agent_interface(self, agent_type, agent_endpoint) -> IssuerAgentInterface:
        """create an issuer agent interface object of the type given"""
        return self.issuer_agent_type_interface_dict[agent_type](agent_endpoint)

    def create_verifier_agent_interface(self, agent_type, agent_endpoint) -> VerifierAgentInterface:
        """create a verifier agent interface object of the type given"""
        print("Verifier agent being added: ", agent_type, " endpoint: ", agent_endpoint)
        return self.verifier_agent_type_interface_dict[agent_type](agent_endpoint)