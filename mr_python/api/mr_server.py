__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

from . scaffold import mr_rest
from ..helpers import utilities


class Auth:
    def __init__(self, rest_server, user, secret, api_key, server_type="mr"):
        self.REST_SERVER = rest_server
        self.SERVER_TYPE = server_type
        self.USER = user
        self.SECRET = secret
        self.API_KEY = api_key

    def login(self):
        return {
            "server_type": self.SERVER_TYPE,
            "user": self.USER,
            "secret": self.SECRET,
            "rest_server": self.REST_SERVER,
            "api_key": self.API_KEY
        }

    def logout(self):
        pass

class BaseObjects:
    def __init__(self, credential):
        self.CRED = credential
        self.rest = mr_rest(credential) # NOTE the class in rest_scaffold might need some work
        self.util = utilities()

    def get_all(self, endpoint):
        return self.rest.get_obj(endpoint)

class Users(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential)

    def get_all(self):
        my_endpoint = "/v1/users/users"
        return super().get_all(my_endpoint)