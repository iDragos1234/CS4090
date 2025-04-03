from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.classical_communication.message import StructuredMessage

'''
NetQASMConnection --> interface between Python and NetQASM 
EPRSocket --> used to store created EPR pairs
Socket --> classical communication channel betwee Alice and Bob
'''


def main(app_config=None):

    # Socket connection to Bob
    socket = Socket('alice', 'bob')

    # EPR socket
    epr_socket = EPRSocket('bob')

    # Connection to NetQASM backend
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )

    with alice:
        # Create a qubit (initialized in the 0 state)
        q = Qubit(alice)

        # Create EPR pair
        # (i.e., the pair of two entangled photons used in entanglement swapping)
        epr = epr_socket.create()[0]  # qubit stored at index 0

        # Teleportation operations
        q.cnot(epr)
        q.H()
        m1 = q.measure()
        m2 = epr.measure()

        # Need to do this if message is sent from the `with` context,
        # due to asynchronicity of the quantum operations (similar to `await`),
        # i.e., waits for quantum operations to be executed.
        alice.flush()

        m1, m2 = int(m1), int(m2)

        message = StructuredMessage(
            header='Corrections',
            payload=(m1, m2),
        )
        socket.send_structured(message)


if __name__ == '__main__':
    main()


