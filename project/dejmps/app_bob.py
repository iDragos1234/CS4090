from dejmps import dejmps_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.logging.output import get_new_app_logger


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

    NUM_SAMPLES = 1

    # Create Bob's context, initialize EPR pairs inside it and call Bob's DEJMPS method.
    # Finally, print out whether Bob successfully created an EPR Pair with Alice.
    with bob:
        # Receive two EPR pairs
        epr1 = epr_socket.recv()[0]
        bob.flush()

        for sample_idx in range(NUM_SAMPLES):
            epr2 = epr_socket.recv()[0]
            bob.flush()

            # Apply DEJMPS circuit for Bob with U_B = Rot_X(3pi/2)
            epr1.rot_X(n=3, d=1)
            epr2.rot_X(n=3, d=1)
            epr1.cnot(epr2)
            bob.flush()

            m_bob = epr2.measure()
            bob.flush()

            # Send Bob's measurement to Alice
            m_bob = int(m_bob)
            socket.send_structured(
                StructuredMessage('m_bob', m_bob)
            )


if __name__ == "__main__":
    main()
