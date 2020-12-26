from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from server.manager.request_manager import PingManager,SearchManager, DownloadManager
import json
from urllib.parse import urlparse


app = Flask(__name__)
api = Api(app)

class PingController(Resource):
    """
    This class handles the ping request of the given ip and port
    """
    def get(self):
        """
        Fetches the local files that are available within the host machine. This searches files
        inside "D:/scripts" folder
        FileName                                                    Size in kb          Host details
        ----------------------------------------------------------------------------------------------------
        d:\scripts\app.xlsx                                         15                  192.168.56.1:1234
        d:\scripts\app1.xlsx                                        22                  192.168.56.1:1234
        d:\scripts\applications_POST_05May2016.xls                  1213                192.168.56.1:1234
        d:\scripts\arg_parser.py                                    0                   192.168.56.1:1234
        d:\scripts\as_new.sql                                       50406               192.168.56.1:1234
        d:\scripts\Blaze.xlsx                                       19                  192.168.56.1:1234
        d:\scripts\blaze_applicationss_POST.xls                     288                 192.168.56.1:1234
        d:\scripts\cc_test_data.xlsx                                46                  192.168.56.1:1234
        d:\scripts\compare_files.py                                 2                   192.168.56.1:1234
        d:\scripts\prebureau_blaze_response.txt                     4                   192.168.56.1:1234
        d:\scripts\t.sql                                            10432               192.168.56.1:1234
        d:\scripts\test_api.txt                                     0                   192.168.56.1:1234
        d:\scripts\~$app1.xlsx                                      0                   192.168.56.1:1234
        d:\scripts\~$Blaze.xlsx                                     0                   192.168.56.1:1234
        :return: List containing the local file details
        """
        ping_obj = PingManager()
        resp = ping_obj.process_get_request()
        return resp


class SearchController(Resource):
    """
    This Class handles the search queries received from the clients
    """
    def get(self):
        """
        First it searches the file locally
        If file not found, then it will do a local zone level search
        If file not found, then it will do a global zone level search
        :return:
        """
        file_name = request.args.get('filename')
        search_handler = SearchManager()
        zone_info = search_handler._SearchManager__get_zone_info(request)
        response = search_handler.process_get_request(file_name, zone_info)
        # print("base url %s" % request.base_url)
        # request_info = urlparse(request.base_url)
        # host_name = request_info.hostname
        # port = request_info.port
        return response

class DownloadFileController(Resource):
    """
    This class handles the Download process of the requested file
    Initiates a Thread for creating a socket and sending the data back to the client asynchronously
    """
    def post(self):
        """
        Process the download request
        :return:
        """
        post_data = request.get_json()
        download_handler = DownloadManager()
        response = download_handler.process_post_request(post_data)
        return response

api.add_resource(PingController, '/ping')  # Route 1
api.add_resource(SearchController, '/search')  # Route 2
api.add_resource(DownloadFileController, '/download')  # Route 3


if __name__ == '__main__':
    app.run(port='5000')