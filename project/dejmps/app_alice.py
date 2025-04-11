import os

from dejmps import dejmps_protocol_alice
from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.logging.output import get_new_app_logger

import numpy as np


def main(app_config=None):
    # Create a socket for classical communication
    socket = Socket('alice', 'bob')

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('bob')

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )

    NUM_ITERATIONS = int(os.getenv('NUM_ITERATIONS', '1'))
    NUM_SAMPLES = 1
    results = []

    # Create Alice's context, initialize EPR pairs inside it and call Alice's DEJMPS method.
    # Finally, print out whether Alice successfully created an EPR Pair with Bob.
    with alice:
        for sample_idx in range(NUM_SAMPLES):
            # Initial EPR pair
            current_epr = epr_socket.create()[0]
            alice.flush()

            success = True
            for _ in range(NUM_ITERATIONS):
                # Create new EPR pair for this iteration
                new_epr = epr_socket.create()[0]
                alice.flush()

                # Apply DEJMPS operations
                current_epr.rot_X(n=1, d=1)
                new_epr.rot_X(n=1, d=1)
                current_epr.cnot(new_epr)
                alice.flush()

                # Measure new_epr and exchange results
                m_alice = int(new_epr.measure())
                socket.send_structured(StructuredMessage("m_alice", m_alice))
                m_bob = int(socket.recv_structured().payload)

                if m_alice != m_bob:
                    success = False
                    break

                # Apply correction if needed
                if m_alice == 1:
                    current_epr.Z()

            if success:
                # Get final state and fidelity
                final_dm = get_qubit_state(current_epr, reduced_dm=False)
                target = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
                fidelity = np.real(np.conj(target) @ final_dm @ target)
                print(f"Fidelity after {NUM_ITERATIONS} iterations: {fidelity}")
                results.append([NUM_ITERATIONS, fidelity])

            print(m_alice, m_bob, fidelity)

    print("Results:", results)



def compute_fidelity(dm, ket):
    """Compute fidelity between a density matrix and a ket state."""
    fidelity = np.conjugate(ket) @ dm @ ket
    assert np.imag(fidelity) == 0
    return np.real(fidelity)


if __name__ == "__main__":
    main()
