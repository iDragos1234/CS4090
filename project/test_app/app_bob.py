from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket


def main(app_config=None):

    # Socket connection to Alice
    socket = Socket('bob', 'alice')

    # EPR socket
    epr_socket = EPRSocket('alice')

    # Connection to NetQASM backend
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )

    with bob:
        # Create EPR pair
        epr = epr_socket.recv()[0]

        # Receive the corrections from ALcie
        message = socket.recv_structured()
        m1, m2 = message.payload

        # Apply corrections
        if m1 == 1:
            epr.Z()
        if m2 == 1:
            epr.X()

        # Check
        result = epr.measure()
        bob.flush()

        print(result)


if __name__ == '__main__':
    main()
