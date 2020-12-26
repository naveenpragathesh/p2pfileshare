from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from server.manager.peer_manager import PeerManager
import json
from urllib.parse import urlparse

app = Flask(__name__)
api = Api(app)

class PeerController(Resource):
    """
    This class handles the active and expired peer list available over the entire network
    """
    def post(self):
        """
        Updates the s3 bucket with the newly added/removed filename and its respective host details
        :return:
        """
        peer_obj = PeerManager()
        post_data = request.get_json()
        resp = peer_obj.process_post_request(post_data.get('filename'),
                                             post_data.get('zone'),
                                             post_data.get('host_details'),
                                             post_data.get('active'))
        return resp

api.add_resource(PeerController, '/updatepeer')


if __name__ == '__main__':
    app.run(port='6000')