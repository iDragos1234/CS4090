import math


def bbpssw_protocol_alice(q1, q2, alice, socket):
    """
    Implements Alice's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    a = bbpssw_gates_and_measurement_alice(q1, q2)
    alice.flush()

    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    # send Alice's result
    socket.send(str(a))

    # get Bob's result
    b = int(socket.recv())

    return a == b


def bbpssw_gates_and_measurement_alice(q1, q2):
    """
    Alice: Apply CNOT(q1 to q2), measure only q2.
    """
    q1.cnot(q2)
    m = q2.measure()
    return m



def bbpssw_protocol_bob(q1, q2, bob, socket):
    """
    Implements Bob's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    b = bbpssw_gates_and_measurement_bob(q1, q2)
    bob.flush()

    # Write below the code to send measurement result to Alice, receive measurement result from Alice and check if protocol was successful
    # get Alice's result
    a = int(socket.recv())

    # send Bob's result
    socket.send(str(b))

    return b == a

def bbpssw_gates_and_measurement_bob(q1, q2):
    """
    Bob: Apply CNOT(q1 to q2), measure only q2.
    """
    q1.cnot(q2)
    m = q2.measure()
    return m

