import os
import socket
from server.downloadfile_socket_listener import send_file
from threading import Thread

class PingManager(object):
    """
    This class handles the ping request and response with a pong data containing the file details
    available within this host
    """
    def process_get_request(self):
        """
        Fetches the local file data in "D:\Scripts" folder
        Appends the host details
        :return:
        """
        local_files = self.__get_local_files_info()
        host_info = self.__add_host_details()
        local_files.append(host_info)
        return local_files

    def __get_local_files_info(self):
        """
        Fetches all the locally available files within "D:\Scripts" folder along with its size
        :return: list containing the file details
        """
        local_file_list = os.listdir('d:\\scripts')
        filepaths = []
        for basename in local_file_list:
            filename = os.path.join('d:\\scripts', basename)
            if os.path.isfile(filename):
                filepaths.append(filename)

        for i in range(len(filepaths)):
            filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i]))
        return filepaths

    def __add_host_details(self):
        """
        Fetches the host ip and port number
        :return:
        """
        host_ip = socket.gethostbyname(socket.gethostname())
        port = 1234
        return {'host_ip': host_ip, 'port': port}



class SearchManager(object):
    def process_get_request(self, filename, zone):
        """
        First it searches the file locally
        If file not found, then it will do a local zone level search
        If file not found, then it will do a global zone level search
        :param filename:
        :param zone:
        :return: dict having the ip and port details of the given filename
        """
        # First search locally
        ping_obj = PingManager()
        local_files = ping_obj._PingManager__get_local_files_info()
        for file_info in local_files:
            if filename == file_info[0].split("\\")[-1]:
                return "File is locally available in this location"+file_info[0]

        # Connect to s3, and get the files in the current zone
        response = self.__search_in_zone(filename, zone)
        if not response:
            # if not available, search other zones
            response = self.__search_in_global_zones(filename)

        # if data is available, return the host details of the requested file, else None
        return {"host_ip": "127.0.0.1", "port": "5000"}

    def __search_in_zone(self, filename, zone):
        """
        Connect to s3, and get the files in the current zone
        Check if the filename is available in the s3 results
        :param filename:
        :param zone:
        :return:
        """
        pass

    def __search_in_global_zones(self, filename):
        """
        Based on ZONE_SEARCH_LEVEL, check the other zones
        S3 data sample format: {'filename': ['192.168.56.102', '192.168.56.103']}
        :param filename:
        :return: {'filename': ['192.168.56.102:1234', '192.168.56.103:5678']}
        """
        pass

    def __get_zone_info(self, request):
        """
        Categorizes the incoming request and sends back the zone info of the request
        :param request:
        :return:
        """
        # returns the zone info of the incoming request
        return "aws-mumbai"


class DownloadManager(object):
    """
    This class handles the Download process of the requested file
    Initiates a Thread for creating a socket and sending the data back to the client asynchronously
    """
    def process_post_request(self, postdata):
        """
        Gets the local full filepath
        Starts the thread to send the file to the client
        :param postdata:
        :return: None
        """
        filename = os.path.join('d:\\scripts', postdata.get('filename'))
        Thread(target=send_file, args=(filename, postdata.get('host_ip'), postdata.get('port'),)).start()
        return None
