import numpy as np
from simulation_utils import *
from typing import Tuple


def bbpssw_protocol(rho_in: np.matrix) -> Tuple[int, int, float]:

    rho = kron([rho_in, rho_in])

    bilateral_cnot = kron([CNOT(), CNOT()])
    rho = Gate(bilateral_cnot)(rho)

    povm = POVM(nqubits=4, meas_qubits=[1, 3], partial_trace=True)
    probs, rho_outs = povm(rho)

    outcome_idx = np.random.choice(len(probs), p=probs)
    outcome_bits = f"{outcome_idx:02b}"
    m_alice, m_bob = int(outcome_bits[0]), int(outcome_bits[1])
    if m_alice != m_bob:
        return m_alice, m_bob, 0.0  # Discard if mismatch


    rho_out = rho_outs[outcome_idx]
    reduced = PartialTrace(nqubits=4, out_qubits=[1, 2, 3])(rho_out)


    phi_plus = bell_state(0, 0)
    f = fidelity(reduced, phi_plus)
    return m_alice, m_bob, f
