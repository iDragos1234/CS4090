from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.classical_communication.message import StructuredMessage


def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket('bob', 'alice')

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('alice')

    # Initialize Bob's NetQASM connectio
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )

    with bob:
        # Receive two EPR pairs
        epr1, epr2, epr3 = epr_socket.recv(number=3)

        # Apply Metwally protocol for Bob with gates U_B = Rot_X(-pi/2)
        epr1.rot_X(n=3, d=1)
        epr2.rot_X(n=3, d=1)

        # Apply Three-to-one protocol gates
        epr3.cnot(epr2)
        epr1.cnot(epr3)

        # Change Bell basis of epr1, epr2 into Z basis
        epr1.cnot(epr2)
        epr1.H()

        # Do Z basis measurements on epr1, epr2
        m_bob_1 = epr1.measure()
        m_bob_2 = epr2.measure()
        bob.flush()

        # Send Bob's measurement to Alice
        m_bob_1, m_bob_2 = int(m_bob_1), int(m_bob_2)
        socket.send_structured(
            StructuredMessage('m_bob', (m_bob_1, m_bob_2))
        )


if __name__ == "__main__":
    main()
