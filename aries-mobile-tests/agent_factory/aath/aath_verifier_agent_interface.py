"""
Absctact Base Class for actual issuer agent interfaces to implement
"""

from agent_factory.verifier_agent_interface import VerifierAgentInterface
import json
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected


class AATHVerifierAgentInterface(VerifierAgentInterface):

    def proof(self):
        """create a proof request """
        pass


