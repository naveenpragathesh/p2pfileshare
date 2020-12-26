import os
import socket

from server.configs.application_config import ZONE_SEARCH_LEVEL

class PeerManager(object):
    """
    Adds/deletes the host details from the s3 bucket of the specific zone
    """
    def process_post_request(self, filename, zone, host_info, active):
        """
        Active param denotes the peer status, and if active is set, then adds the host info to the
        s3 bucket of the given zone, else deletes the host info from the s3 bucket
        :param filename:
        :param zone:
        :param host_info:
        :param active: boolean to denote the status of the peer
        :return:
        """
        if active:
            # Adds the host details to s3, with the newly downloaded filename
            pass
        else:
            # Deletes the host details from s3, for the given filename
            pass