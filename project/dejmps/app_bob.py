from dejmps import dejmps_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.logging.output import get_new_app_logger


def main(app_config=None):
    # log_config = app_config.log_config
    # app_logger = get_new_app_logger(app_name="sender", log_config=log_config)

    # Create a socket for classical communication
    socket = Socket(
        'bob', 'alice',
        # log_config=log_config,
    )

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('alice')

    # Initialize Bob's NetQASM connectio
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
        # log_config=log_config,
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's DEJMPS method.
    # Finally, print out whether Bob successfully created an EPR Pair with Alice.
    with bob:
        # Receive two EPR pairs
        epr1 = epr_socket.recv()[0]
        epr2 = epr_socket.recv()[0]

        # Apply DEJMPS circuit for Bob with U_B = Rot_X(3pi/2)
        epr1.rot_X(n=3, d=1)
        epr2.rot_X(n=3, d=1)
        epr1.cnot(epr2)
        m_bob = epr2.measure()

        bob.flush()  # NOTE: Flush before doing any further operations within this `with`!

        # Send Bob's measurement to Alice
        m_bob = int(m_bob)
        socket.send_structured(
            StructuredMessage('m_bob', m_bob)
        )


if __name__ == "__main__":
    main()
