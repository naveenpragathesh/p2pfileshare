import requests

import json
import os
import sys
import socket
import traceback
import uuid
import tqdm
from datetime import datetime


import requests
from requests.auth import HTTPDigestAuth

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 100

class Service_Connector():
    """
    This class takes care of connecting with the external API's
    """

    def __init__(self):
        self.service_map = {
            'get': requests.get,
            'put': requests.put,
            'post': requests.post,
            'delete': requests.delete}

    def connect_service(self, method, url, data=None, params=''):
        """
        Makes the API calls based on the given inout params
        :param method: GET/POST/PUT
        :param url: Endpoint url
        :param data: POST/PUT data
        :param params: Query parameters
        :return: json response
        """
        retry = 3
        timeout = 60
        headers = {}
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'

        if 'Content-Type' not in headers:
            if method != 'get':
                headers['Content-Type'] = 'application/json'
            else:
                headers['Content-Type'] = None
        trial = 0
        response = None
        try:
            while trial < retry:
                try:
                    trial = trial + 1
                    response = self.service_map[method](
                        url,
                        headers=headers,
                        data=data,
                        params=params,
                        timeout=timeout,
                        verify=False)
                    break

                except Exception:
                    trial = trial + 1
                    print(
                    "Unknown exception happened while connecting to the %s method ff the URL %s with exception %s",
                    method, url.split("?")[0], str(traceback.format_exc()))
        except Exception:
            print("Exception occurred")
        finally:
            return response



class P2PFileSharing(object):
    """
    This is the entry point script for the client to interact with the peers available over the network
    """
    def __init__(self):
        pass

    def process_ping(self, ip="127.0.0.1", port="5000"):
        """
        Connects to the ping url of the specified host ip and port
        :param ip:
        :param port:
        :return: pong data - json response
        """
        try:
            service_conn_obj = Service_Connector()
            url = "http://"+ip+":"+port+"/ping"
            print("Connecting to ping url %s..." %url)
            response = service_conn_obj.connect_service("get", url)
            return response.json()
        except Exception:
            print("Exception occurred in process_ping %s" %str(traceback.format_exc()))

    def process_search(self, file_name, ip="127.0.0.1", port="5000"):
        """
        Connects to the search url of the specified host ip and port
        :param file_name:
        :param ip:
        :param port:
        :return: SearchHit response containing the ip and port details of the given filename
        """
        try:
            service_conn_obj = Service_Connector()
            url = "http://" + ip + ":" + port + "/search?filename=" + file_name
            print("Connecting to search url %s..." % url)
            response = service_conn_obj.connect_service("get", url)
            return response.json()
        except Exception:
            print("Exception occurred in process_search %s" %str(traceback.format_exc()))

    def update_s3_peer_info(self, file_name, ip, port, is_active):
        """
        Connects to the updatepeer url of the specified host ip and port
        Either updates or deletes the entry based on the is_active field
        """
        try:
            service_conn_obj = Service_Connector()
            url = "http://" + ip + ":" + port + "/updatepeer"
            data = {
                "filename": file_name,
                "host_ip": host_ip,
                "port": port,
                "active": is_active
            }
            print("Connecting to search url %s..." % url)

            service_conn_obj.connect_service("post", url, data=json.dumps(data))
            return response.json()
        except Exception:
            print("Exception occurred in update_s3_peer_info %s" %str(traceback.format_exc()))


    def process_download(self, file_name, host_ip="127.0.0.1", port="5000"):
        """
        Creates a socket and listens for any incoming data
        Connects to download API and initiates the download process
        :param file_name:
        :param host_ip:
        :param port:
        :return: Nothing, File will be stored in "D:/socket_download" folder
        """
        try:
            s = socket.socket()
            s.bind((host_ip, 5001))
            s.listen(5)
            print("[*] Listening as %s:%s" % (host_ip, 5001))
            service_conn_obj = Service_Connector()
            url = "http://" + host_ip + ":" + port + "/download"
            data = {
                "filename": file_name,
                "host_ip": host_ip,
                "port": 5001
            }
            print("Connecting to search url %s..." % url)

            service_conn_obj.connect_service("post", url, data=json.dumps(data))

            client_socket, address = s.accept()

            print("[+] connected with %s:%s" % (address[0], address[1]))

            received = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            progress = tqdm.tqdm(range(filesize), "Receiving " + filename, unit="B", unit_scale=True, unit_divisor=50)
            with open("d:\\socket_download\\" + filename, "wb") as f:
                for _ in progress:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))

            print("\n\n -------------------Download completed----------------------\n\n")
            # make an api call to peerlist, and add the filename and respective ip details to s3 bucket
            # self.update_s3_peer_info(filename, host_ip, port, True)
            client_socket.close()
            s.close()
        except Exception:
            print("Exception occurred in process_download %s" %str(traceback.format_exc()))



if __name__=="__main__":
    p2p_obj = P2PFileSharing()
    while True:
        print("Select any one below")
        print("1. Ping")
        print("2. Search")
        print("3. Download")
        print("4. Exit")
        option = input()
        if option in ["1"] or option.lower() in ["ping"]:
            print("Select any one below(enter option number)")
            print("1. Enter host IP and port details")
            print("2. Connect with default IP")
            ping_option = input()
            if ping_option == "1":
                # validate the IP and port
                print("Enter IP details, sample format 192.168.56.102:5000")
                ip_details = input()
                ip = ip_details.split(":")[0]
                port = ip_details.split(":")[1]
                print("Connecting to host(%s) and port(%s).." %(ip, port))
                resp = p2p_obj.process_ping(ip, port)
                host_details = resp.pop()
                print("FileName" + " " * 52 + "Size in kb" + " " * 10 + "Host details")
                print("-" * 100)
                for file_info in resp:
                    print(file_info[0] + " " * (60 - len(file_info[0])) + str(int(file_info[1] / 1024)) + " " * (
                    20 - len(str(int(file_info[1] / 1024)))) + host_details.get('host_ip') + ":" + str(
                        host_details.get('port')))

            else:
                # connects to default ip
                print("Connecting to default host(127.0.0.1) and port(5000)..")
                resp = p2p_obj.process_ping()
                host_details = resp.pop()
                print("FileName"+" "*52 +"Size in kb"+" "*10 +"Host details")
                print("-"*100)
                for file_info in resp:
                    print(file_info[0] + " "*(60-len(file_info[0])) + str(int(file_info[1]/1024)) + " "*(20-len(str(int(file_info[1]/1024)))) + host_details.get('host_ip')+":"+str(host_details.get('port')))

        elif option in ["2"] or option.lower() in ["search"]:
            print("Enter filename to search")
            filename_option = input()
            print("\n\n")
            resp = p2p_obj.process_search(filename_option)
            print("\n\n-------------Search results-----------------")
            print(resp)
        elif option in ["3"] or option.lower() in ["download"]:
            print("Enter filename")
            filename_option = input()
            print("Enter IP and port, seperated by :")
            host_ip, host_port = input().split(":")
            resp = p2p_obj.process_download(filename_option, host_ip, host_port)
        elif option in ["4"]:
            # If the client is terminating, then remove the peer from the active peer list by making an api call
            # self.update_s3_peer_info(filename, host_ip, port, False)
            print("Exiting the terminal........")
            sys.exit()
