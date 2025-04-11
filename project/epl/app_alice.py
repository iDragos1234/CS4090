from epl import epl_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.qubit import Qubit
from netqasm.sdk.classical_communication.message import StructuredMessage

def main(app_config=None):
    # Create a socket for classical communication
    socket = Socket("alice", "bob", app_config=app_config)
    # Create an EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's connection
    with NetQASMConnection(
            "alice",
            app_config=app_config,
            epr_sockets=[epr_socket],
    ) as alice:
        # Create two EPR pairs
        q1 = epr_socket.create_keep()[0]
        q2 = epr_socket.create_keep()[0]

        # Run EPL protocol
        success = epl_protocol_alice(q1, q2, alice, socket)
        print(f"EPL protocol success: {success}")


if __name__ == "__main__":
    main()
