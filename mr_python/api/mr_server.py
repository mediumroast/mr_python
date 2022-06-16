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
    def __init__(self, credential, obj_type, api_version='v1'):
        self.CRED = credential
        self.rest = mr_rest(credential) # NOTE the class in rest_scaffold might need some work
        self.util = utilities()
        self.OBJ_TYPE = obj_type
        self.API_VERSION = api_version

    def get_all(self, endpoint='getall'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        return self.rest.get_obj(full_endpoint)

    def get_by_name(self, name, endpoint='getbyx'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        my_obj = {'getByX': 'name', 'xEquals': name}

    def get_by_id(self, id, endpoint='getbyx'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        my_obj = {'getByX': 'id', 'xEquals': id}

    def get_by_x(self, attribute, value, endpoint='getbyx'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        my_obj = {'getByX': attribute, 'xEquals': value} 

    def create_obj(self, obj, endpoint='register'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        return self.rest.post_obj(full_endpoint, obj)
        
    def update_obj(self, id, obj, endpoint):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])

    def delete_obj(self, id, endpoint):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])     

class Users(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='users')

    def get_all(self):
        return super().get_all(endpoint='users')

class Studies(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='studies')

class Companies(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='companies')

class Interactions(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='interactions')