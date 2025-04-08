from dejmps import dejmps_protocol_alice
from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.logging.output import get_new_app_logger

import numpy as np


def main(app_config=None):
    # log_config = app_config.log_config
    # app_logger = get_new_app_logger(app_name="sender", log_config=log_config)

    # Create a socket for classical communication
    socket = Socket(
        'alice', 'bob',
        # log_config=log_config,
    )

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('bob')

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
        # log_config=log_config,
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's DEJMPS method.
    # Finally, print out whether Alice successfully created an EPR Pair with Bob.
    with alice:
        # Create two EPR pairs
        epr1 = epr_socket.create()[0]
        epr2 = epr_socket.create()[0]

        # Apply DEJMPS circuit for Alice with U_A = Rot_X(pi/2)
        epr1.rot_X(n=1, d=1)
        epr2.rot_X(n=1, d=1)
        epr1.cnot(epr2)
        m_alice = epr2.measure()

        alice.flush()  # NOTE: Flush before doing any further operations within this `with`!

        # Collect Alice's and Bob's measurements
        m_alice = int(m_alice)
        m_bob = int(socket.recv_structured().payload)

        # Get the density matrix of the output EPR pair
        epr1_dm = get_qubit_state(epr1, reduced_dm=False)

        # Compute fidelity wrt. target state (i.e., the pure Bell state)
        target_state = 1 / np.sqrt(2) * np.array([1, 0, 0, 1], dtype=complex)
        fidelity = compute_fidelity(epr1_dm, target_state)

        debug_message = f'DEJMPS Simulation:\n'\
                        f'------------------\n'\
                        f'Measurements: m_alice = {m_alice}, m_bob = {m_bob};\n'\
                        f'Successful? {m_alice == m_bob};\n'\
                        f'EPR_out state: \n{np.round(epr1_dm, 5)};\n'\
                        f'Target state: \n{np.round(target_state, 5)};\n'\
                        f'Fidelity: {fidelity};\n'

        # app_logger.log(debug_message)

        # Output simulation results in the following standard format:
        # `(m_alice, m_bob, fidelity)`
        print(m_alice, m_bob, fidelity)


def compute_fidelity(dm, ket):
    """Compute fidelity between a density matrix and a ket state."""
    fidelity = np.conjugate(ket) @ dm @ ket
    assert np.imag(fidelity) == 0
    return np.real(fidelity)


if __name__ == "__main__":
    main()
