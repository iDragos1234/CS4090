from dejmps import dejmps_protocol_alice
from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.external import get_qubit_state
from netqasm.logging.output import get_new_app_logger


def main(app_config=None):
    log_config = app_config.log_config
    app_logger = get_new_app_logger(app_name="sender", log_config=log_config)

    # Create a socket for classical communication
    socket = Socket('alice', 'bob', log_config=log_config)

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('bob')

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
        log_config=log_config,
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's DEJMPS method.
    # Finally, print out whether Alice successfully created an EPR Pair with Bob.
    with alice:
        epr1 = epr_socket.create()[0]
        epr2 = epr_socket.create()[0]

        # U_A = Rot_X(pi/2)
        epr1.rot_X(n=1, d=1)
        epr2.rot_X(n=1, d=1)
        epr1.cnot(epr2)
        m_alice = epr2.measure()

        alice.flush()
        m_alice = int(m_alice)

        message = StructuredMessage(
            header='m_alice',
            payload=m_alice,
        )
        socket.send_structured(message)

        response = socket.recv_structured()
        m_bob = response.payload if message.header == 'm_bob' else None

        print(f'Alice has the following measurements: m_alice = {m_alice}, m_bob = {m_bob}.')
        print(f'DEJMPS successful? {m_alice == m_bob}.')
        print(f'EPR_out state: {get_qubit_state(epr1)}.')

        # original = qubit_from(phi, theta)
        # original_dm = to_dm(original)
        # fidelity = get_fidelity(original, dm)
        # print(f"fidelity {fidelity}")


if __name__ == "__main__":
    main()
