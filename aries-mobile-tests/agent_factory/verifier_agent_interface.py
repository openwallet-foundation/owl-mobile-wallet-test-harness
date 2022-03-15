"""
Absctact Base Class for actual verifier agent interfaces to implement
"""

from abc import ABC, abstractmethod

class VerifierAgentInterface(ABC):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    @abstractmethod
    def proof(self):
        """do a proof request"""


