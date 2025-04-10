from bbpssw import bbpssw_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):
    socket = Socket("the_hague", "delft")
    epr_socket = EPRSocket("delft")

    with NetQASMConnection(app_config=app_config, epr_sockets=[epr_socket]) as bob:
        q1, q2 = epr_socket.recv(number=2)
        success = bbpssw_protocol_bob(q1, q2, bob, socket)
        print("Bob: BBPSSW success:", success)

if __name__ == "__main__":
    main()
