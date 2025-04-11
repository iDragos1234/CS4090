import math

from netqasm.sdk.classical_communication.message import StructuredMessage


def epl_protocol_alice(q1, q2, alice, socket):
    """
    Implements Alice's side of the EPL distillation protocol.
    This function should perform the gates and measurements for EPL using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    a = epl_gates_and_measurement_alice(q1, q2)
    alice.flush()

    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful

    # # Requires two iterations? pseudocode
    # outcomes = []
    # for _ in range(2):
    #     a = epl_gates_and_measurement_alice(q1, q2, client)
    #     alice.flush()
    #     outcomes.append(a.get())
    #
    # # Compare parity of outcomes across iterations
    # parity = (outcomes[0] + outcomes[1]) % 2
    # socket.send_parity(parity)
    # bob_parity = socket.recv_parity()
    # return parity == bob_parity


    # Get measurement result
    a_result = int(a.get())
    # Send result to Bob and receive Bob's result
    socket.send_structured(StructuredMessage("alice_measurement", a_result))
    b_result = socket.recv_structured().payload
    # Check if results match
    return a_result == b_result


def epl_gates_and_measurement_alice(q1, q2):
    """
    Performs the gates and measurements for Alice's side of the EPL protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :return: Integer 0/1 indicating Alice's measurement outcome
    """
    # Apply Y-rotation to brokers (step 2)
    q1.rot_Y(angle=math.pi / 2)
    q2.rot_Y(angle=math.pi / 2)

    # CZ gate between broker and client (step 3)
    q1.cphase(client_q)

    # Measure in X-basis (step 4)
    q2.h()
    return q2.measure()


def epl_protocol_bob(q1, q2, bob, socket):
    """
    Implements Bob's side of the EPL distillation protocol.
    This function should perform the gates and measurements for EPL using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    b = epl_gates_and_measurement_bob(q1, q2)
    bob.flush()

    # Write below the code to send measurement result to Alice, receive measurement result from Alice and check if protocol was successful
    # Get measurement result
    b_result = int(b.get())
    # Receive Alice's result and send own result
    a_result = socket.recv_structured().payload
    socket.send_structured(StructuredMessage("bob_measurement", b_result))
    # Check if results match
    return a_result == b_result

def epl_gates_and_measurement_bob(q1, q2):
    """
    Performs the gates and measurements for Bob's side of the EPL protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :return: Integer 0/1 indicating Bob's measurement outcome
    """
    q1.cnot(q2)
    return q2.measure()

