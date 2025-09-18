from dataclasses import dataclass
import numpy as np

from quark.core import Core, Result, Data
from quark.interface_types import Other

from sc.quark.qaptiva.qaptiva_qds import ProbabilityDistribution

def hellinger(p1, p2):
    assert len(p1) == len(p2)
    return np.sqrt(np.sum((np.sqrt(p1) - np.sqrt(p2))**2))/np.sqrt(2.0)

@dataclass
class GHZ(Core):

    size:int

    def expected_prob(self, state):
        if isinstance(state, list):
            state = "".join([str(s) for s in state])
        size = self.size
        if state == size*'1':
            return 0.5
        elif state == size*'0':
            return 0.5
        else:
            return 0.0
    
    def preprocess(self, data):
        return Data(Other({"size": self.size}))
        
    def postprocess(self, data:Other[ProbabilityDistribution]) -> Result:
        assert isinstance(data, Other) and isinstance(data.data, ProbabilityDistribution)
        self.result:ProbabilityDistribution = data.data
        p1 = [] 
        p2 = []
        for state, prob in self.result.prob_dict.items():
            p1.append(prob)
            p2.append(self.expected_prob(state))
        self.hel = hellinger(p1, p2)
        return Data(Other(self.hel))

    def get_metrics(self):
        metrics = super().get_metrics()
        metrics["probabilities"] = self.result.prob_dict
        metrics["HD"] = self.hel
        return metrics
