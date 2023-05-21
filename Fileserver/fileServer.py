import socket
from emailFunction import sendEmail 
import aesFunction as aes

import os

s = ""
IP = socket.gethostbyname(s)
"""Die untenstehende IP zum Testen"""
IP = "127.0.0.1"
PORT = 8367
ADDR = (IP, PORT)
Format = "utf-8"
ONLINE = True
CONN_ALIVE = True

def setONLINE(b: bool):
    global ONLINE
    ONLINE = b

def getONLINE() -> bool:
    global ONLINE
    return(ONLINE)

def setCONN_ALIVE(b: bool):
    global CONN_ALIVE
    CONN_ALIVE = b

def getCONN_ALIVE() -> bool:
    global CONN_ALIVE
    return(CONN_ALIVE)

"""DIR is not allowed to change"""
DIR = os.getcwd() + "\\STORAGE"

"""navDir tracks the navigation"""
navDir = DIR

def setNavDir(localNavDir):
    global navDir
    navDir = localNavDir

def getNavDir():
    global navDir
    return navDir

def sendData(conn, msg):
    conn.send(aes.encrypt(msg))

def recvData(conn):
    msg = aes.decrypt(conn.recv(1024)).decode("utf-8")
    return msg


"""Command Navitgations"""
def download():
    """$dw"""
    pass
        
def upload():
    """$up"""
    pass
        
def ls(conn):
    """$ls"""
    currentDir = "\"" + navDir[len(DIR) : len(navDir)] + "\""
    if currentDir != "\"\"":
        currentDir += "\n[0]   Get Back"
    subDir = os.listdir(navDir)
    subDir = [f"[{index}] .\\" + subDir[index - 1] if os.path.isdir(navDir + "\\" + subDir[index -1]) else f"[{index}]   " + subDir[index -1] for index in range(1, len(subDir) + 1)]
    subDir = f"\n[Current Dir] {currentDir}\n" + "\n".join(subDir)
    sendData(conn, subDir)
    
        
def cd(conn, msg):
    """$cd"""
    navDir = getNavDir()
    subDir = os.listdir(navDir)
    try:
       index = int(msg[4:])
    except Exception:
        sendData(conn, "Not a correct Path selected")
    else:
        if index == 0:
            if (len(navDir) > len(DIR)):
                navDir = navDir[len(DIR) + 1 : len(navDir)]
                navDir = DIR + "\\" + "\\".join("\\".split(navDir)[0:-1])
                if navDir[len(navDir)-1] == "\\":
                    navDir = navDir[0 : len(navDir) - 1]
                    setNavDir(navDir)
                #"""The below try execept may not be needed"""
                try:
                    ls(conn)
                except Exception:
                    sendData(conn, "This directory is not existing")
            else:
                sendData(conn, "You cant go further back")
        else:
            try:
                print(index)
                navDir = os.path.join(navDir, subDir[index - 1])
            except IndexError:
                sendData(conn, "This Index does not Exist")
            else:
                if os.path.isdir(navDir):
                    setNavDir(navDir)
                    ls(conn)
                else:
                    sendData(conn, "This is not a directory but a file. Try dw to download this file.")

def cancel():
    """$cc"""
    pass

def shutdown(conn):
    """$sd"""
    sendData(conn, "False")
    conn.close()
    setONLINE(False)
    setCONN_ALIVE(False)

def disconnect(conn):
    """$dc"""
    sendData(conn, "False")
    conn.close()
    setCONN_ALIVE(False)

def command(conn, msg):
    """Kommandlogik"""
    if len(msg) > 2:
        print(msg)
        com = msg[0:3]
        if com == "$dw":
            download()
        elif com == "$up":
            upload()
        elif com == "$ls":
            ls(conn)
        elif com == "$cd":
            cd(conn, msg)
        elif com == "$cc":
            cancel()
        elif com == "$sd":
            shutdown(conn)
        elif com == "$dc":
            disconnect(conn)
        else:
            sendData(conn, "This Command is unknown")
    else:
        sendData(conn, "Empty Command")
        

def main():
    print("Server ist am Starten")
    """Server TCP Socket"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = socket.gethostbyname(s)
    server.bind(ADDR)
    server.listen()
    print(f"Server gestartet... \n[ADDR] {ADDR}")

    """Main LOOP"""
    while ONLINE:
        navDir = setNavDir(DIR)
        conn, addr = server.accept()
        print(f"[New Connection] {addr} connected")
        #sendEmail(addr) // add Emailcredentials 
        setCONN_ALIVE(True)
        while(getCONN_ALIVE()):
            msg = recvData(conn)
            sendData(conn, ">" + msg + "<")
            command(conn, msg)
            
        

if __name__ == "__main__":
    main()
