# Copyright (c) 2025 Science + Computing AG / Eviden SE (Atos Group)
#
# This file is part of the QUARK benchmarking framework.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
# Contact: stefan-raimund.maschek@eviden.com


from dataclasses import dataclass
import numpy as np

from quark.core import Core, Result, Data
from quark.interface_types import Other, SampleDistribution

from quark.interface_types.circuit import Circuit
from quark.interface_types.quantum_result import SampleDistribution

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
        
    def postprocess(self, data:SampleDistribution) -> Result:
        assert isinstance(data, SampleDistribution)
        self.result:SampleDistribution = data
        p1 = [] 
        p2 = []
        for state, prob in self.result.as_list():
            p1.append(prob)
            p2.append(self.expected_prob(state))
        self.hel = hellinger(p1, p2)
        return Data(Other(self.hel))

    def get_metrics(self):
        metrics = super().get_metrics()
        metrics["probabilities"] = self.result.as_list()
        metrics["HD"] = self.hel
        return metrics


@dataclass
class GHZtoQasmCircuit(Core):
    measure: bool = False

    def preprocess(self, data:Other[dict]) -> Result:
        n: dict = data.data.get("size")
        header = f"""
        OPENQASM 3.0;
        qubit q[{n}];
        bit c[{n}];
        """
        circuit = "h q[0];" + \
            "\n".join([f"cx q[{i}],q[{i+1}];" for i in range(n-1)])
        measurement = "" if not self.measure else "\n".join(
            [f"measure q[{i}] -> c[{i}];" for i in range(n)])


        return Data(Circuit(header + circuit + measurement))

    def postprocess(self, data: SampleDistribution):
        assert isinstance(data, SampleDistribution)
        return Data(data)
