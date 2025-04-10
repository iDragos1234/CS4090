from bbpssw import bbpssw_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):
    socket = Socket("delft", "the_hague")
    epr_socket = EPRSocket("the_hague")

    with NetQASMConnection(app_config=app_config, epr_sockets=[epr_socket]) as alice:
        q1, q2 = epr_socket.create(number=2)
        success = bbpssw_protocol_alice(q1, q2, alice, socket)
        print("Alice: BBPSSW success:", success)

if __name__ == "__main__":
    main()
