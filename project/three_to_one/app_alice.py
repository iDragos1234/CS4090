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
        # Create three EPR pairs
        epr1, epr2, epr3 = epr_socket.create(number=3)

        # Apply Metwally protocol for ALice with gates U_A = Rot_X(pi/2)
        epr1.rot_X(n=1, d=1)
        epr2.rot_X(n=1, d=1)

        # Apply Three-to-one protocol gates
        epr3.cnot(epr2)
        epr1.cnot(epr3)

        # Change Bell basis of epr1, epr2 into Z basis
        epr1.cnot(epr2)
        epr1.H()

        # Do Z basis measurements on epr1, epr2
        m_alice_1 = epr1.measure()
        m_alice_2 = epr2.measure()
        alice.flush()

        # Collect Bob's measurements
        m_bob_1, m_bob_2 = socket.recv_structured().payload

        # Convert Alice's and Bob's Z basis measurements into ZZ basis measurements
        # (equivalent to measurements in the Bell state) of their respective epr1, epr2 qubits
        m_alice_1, m_alice_2 = int(m_alice_1),  int(m_alice_2)
        m_bob_1, m_bob_2 = int(m_bob_1), int(m_bob_2)

        # Get the density matrix of the output EPR pair (i.e., epr3)
        epr3_dm = get_qubit_state(epr3, reduced_dm=False)

        # Compute fidelity wrt. target state (i.e., the pure Bell state)
        target_state = 1 / np.sqrt(2) * np.array([1, 0, 0, 1], dtype=complex)  # |\phi_{00}> Bell state
        fidelity = compute_fidelity(epr3_dm, target_state)

        # Output simulation results in the following format:
        print(m_alice_1, m_alice_2, m_bob_1, m_bob_2, fidelity)


def compute_fidelity(dm, ket):
    """Compute fidelity between a density matrix and a ket state."""
    fidelity = np.conjugate(ket) @ dm @ ket
    assert np.imag(fidelity) == 0
    return np.real(fidelity)


if __name__ == "__main__":
    main()
