import socket
import tqdm
import os
from time import sleep

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 100

def send_file(filename, host, port):
    """
    Creates the socket with the given host and port details
    Transfers the data from server to the client
    :param filename:
    :param host:
    :param port:
    :return: Nothing
    """
    filesize = os.path.getsize(filename)
    s = socket.socket()
    print("[+] Connecting to %s:%s" %(host, port))
    s.connect((host, port))
    print("[+] Connected.")
    msg = str(filename+SEPARATOR+str(filesize)).encode()
    s.send(msg)
    progress = tqdm.tqdm(range(filesize), "Sending "+filename, unit="B", unit_scale=True, unit_divisor=50)
    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()