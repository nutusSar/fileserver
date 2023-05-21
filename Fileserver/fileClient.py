import socket
import aesFunction as aes

IP = "127.0.0.1"
PORT = 8367
ADDR = (IP, PORT)
FORMTAT = "utf-8"
CONN_ALIVE = True

def setCONN_ALIVE(b: bool):
    global CONN_ALIVE
    CONN_ALIVE = b

def getCONN_ALIVE():
    global CONN_ALIVE
    return(CONN_ALIVE)

def sendData(client, msg):
    client.send(aes.encrypt(msg))

def recvData(client):
    msg = aes.decrypt(client.recv(1024)).decode("utf-8")
    return msg

def Test():
    """ Starting TCP socket"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Connected")
    sendData(client, "$ls")
    print("[SERVER] " + recvData(client))
    print("[SERVER] " + recvData(client))
    sendData(client, "$cd 2")
    print("[SERVER] " + recvData(client))
    print("[SERVER] " + recvData(client))


def main():
    """Starting TCP socket"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Connected")
    while(getCONN_ALIVE()):
        try:
            uMsg = input(">Enter Command:< ")
            uMsg = str (uMsg)
        except Exception:
            print(Exception)
        else:
            sendData(client, uMsg)
            print("[SERVER] " + recvData(client))
            state = recvData(client)
            if state == "False":
                setCONN_ALIVE(False)
                print("[SERVER] " + "Closed Connection")
            else:
                print("[SERVER] " + state)


if __name__ == "__main__":
    main()
