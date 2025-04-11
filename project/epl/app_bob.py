from epl import epl_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.qubit import Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage


def main(app_config=None):
    # Create a socket for classical communication
    socket = Socket("bob", "alice", app_config=app_config)
    # Create an EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Bob's conn
    with NetQASMConnection(
            "bob",
            app_config=app_config,
            epr_sockets=[epr_socket],
    ) as bob:
        # Receive two EPR pairs
        q1 = epr_socket.recv_keep()[0]
        q2 = epr_socket.recv_keep()[0]

        # Run EPL protocol
        success = epl_protocol_bob(q1, q2, bob, socket)
        print(f"EPL protocol success: {success}")


if __name__ == "__main__":
    main()
