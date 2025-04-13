from netqasm.sdk import EPRSocket, Qubit
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state

import numpy as np

def main(app_config=None):
    socket = Socket('alice', 'bob')
    epr_socket = EPRSocket('bob')
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )
    with alice:
        epr1, epr2 = epr_socket.create(number=2)

        # BBPSSW circuit, # CNOT: control epr1, target epr2, then measure 2
        epr1.cnot(epr2)
        m_alice = epr2.measure()

        alice.flush()

        m_alice = int(m_alice)
        m_bob = int(socket.recv_structured().payload)

        # protocol success check
        success = (m_alice == m_bob)
        if success:
            combined_dm = get_qubit_state([epr1], reduced_dm=False)

            # Target Bell state is |phi00⟩ = (|00⟩ - |11⟩)/√2
            target_state = 1 / np.sqrt(2) * np.array([1, 0, 0, 1], dtype=complex)
            fidelity = np.abs(target_state.conj().T @ combined_dm @ target_state).real
        else:
            fidelity = 0.0

        print(m_alice, m_bob, fidelity)


if __name__ == "__main__":
    main()
