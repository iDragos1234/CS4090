from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state

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

    with alice:
        # Create two EPR pairs
        epr1, epr2 = epr_socket.create(number=2)

        # Apply DEJMPS circuit for Alice with U_A = Rot_X(pi/2)
        epr1.rot_X(n=1, d=1)  # U_A
        epr2.rot_X(n=1, d=1)  # U_A
        epr1.cnot(epr2)       # CNOT
        m_alice = epr2.measure()
        alice.flush()

        # Collect Alice's and Bob's measurements
        m_alice = int(m_alice)
        m_bob = int(socket.recv_structured().payload)

        # Get the density matrix of the output EPR pair
        epr1_dm = get_qubit_state(epr1, reduced_dm=False)

        # Compute fidelity wrt. target state (i.e., the pure Bell state)
        target_state = 1 / np.sqrt(2) * np.array([1, 0, 0, 1], dtype=complex)  # |\phi_{00}> Bell state
        fidelity = compute_fidelity(epr1_dm, target_state)

        debug_message = f'DEJMPS Simulation:\n'\
                        f'------------------\n'\
                        f'Measurements: m_alice = {m_alice}, m_bob = {m_bob};\n'\
                        f'Successful? {m_alice == m_bob};\n'\
                        f'EPR_out state: \n{np.round(epr1_dm, 5)};\n'\
                        f'Target state: \n{np.round(target_state, 5)};\n'\
                        f'Fidelity: {fidelity};\n'

        # Output simulation results in the following format:
        print(m_alice, m_bob, fidelity)


def compute_fidelity(dm, ket):
    """Compute fidelity between a density matrix and a ket state."""
    fidelity = np.conjugate(ket) @ dm @ ket
    assert np.imag(fidelity) == 0
    return np.real(fidelity)


if __name__ == "__main__":
    main()
