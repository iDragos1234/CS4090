from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.classical_communication.message import StructuredMessage

def main(app_config=None):
    socket = Socket('bob', 'alice')
    epr_socket = EPRSocket('alice')
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )
    with bob:
        epr1, epr2 = epr_socket.recv(number=2)

        epr1.cnot(epr2)  # CNOT: control epr1, target epr2
        m_bob = epr2.measure()

        bob.flush()

        m_bob = int(m_bob)
        socket.send_structured(StructuredMessage('m_bob', m_bob))

if __name__ == "__main__":
    main()