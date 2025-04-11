import os

from dejmps import dejmps_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.logging.output import get_new_app_logger


def main(app_config=None):
    NUM_ITERATIONS = int(os.getenv('NUM_ITERATIONS', '1'))

    # Create a socket for classical communication
    socket = Socket('bob', 'alice')

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('alice')

    # Initialize Bob's NetQASM connectio
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )

    NUM_ITERATIONS = int(os.getenv("NUM_ITERATIONS", 1))  # Read iterations

    # Create Bob's context, initialize EPR pairs inside it and call Bob's DEJMPS method.
    # Finally, print out whether Bob successfully created an EPR Pair with Alice.
    with bob:
        for _ in range(1):  # Single sample per configuration
            current_epr = epr_socket.recv()[0]
            bob.flush()

            success = True
            for _ in range(NUM_ITERATIONS):
                new_epr = epr_socket.recv()[0]
                bob.flush()

                # Apply Bob's operations
                current_epr.rot_X(n=3, d=1)  # Rot_X(-π/2)
                new_epr.rot_X(n=3, d=1)
                current_epr.cnot(new_epr)
                bob.flush()

                # Measure and exchange results
                m_bob = int(new_epr.measure())
                socket.send_structured(StructuredMessage("m_bob", m_bob))
                m_alice = int(socket.recv_structured().payload)

                if m_alice != m_bob:
                    success = False
                    break

                # Apply correction if needed
                if m_bob == 1:
                    current_epr.Z()


if __name__ == "__main__":
    main()
