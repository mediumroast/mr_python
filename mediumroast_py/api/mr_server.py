__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-September-04'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."


from . scaffold import mr_rest
from ..helpers import utilities

class Auth:
    def __init__(self, rest_server, user, secret, api_key):
        self.REST_SERVER = rest_server
        self.USER = user
        self.SECRET = secret
        self.API_KEY = api_key

    def login(self):
        return {
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
        self.rest = mr_rest(credential)
        self.util = utilities()
        self.OBJ_TYPE = obj_type
        self.API_VERSION = api_version

    def get_all(self, endpoint='getall'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        return self.rest.get_obj(full_endpoint)

    def find_by_name(self, name, endpoint='findbyx'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        my_obj = {'findByX': 'name', 'xEquals': name}
        return self.rest.post_obj(full_endpoint, my_obj, return_json=True)

    def find_by_id(self, id, endpoint='findbyx'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        my_obj = {'findByX': 'id', 'xEquals': id}
        return self.rest.post_obj(full_endpoint, my_obj, return_json=True)

    def find_by_x(self, attribute, value, endpoint='findbyx'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        my_obj = {'findByX': attribute, 'xEquals': value} 
        return self.rest.post_obj(full_endpoint, my_obj, return_json=True)

    def create_obj(self, obj, endpoint='register'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        return self.rest.post_obj(full_endpoint, obj)
        
    def update_obj(self, obj, endpoint='update'):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        return self.rest.post_obj(full_endpoint, obj)

    def delete_obj(self, id, endpoint):
        full_endpoint = '/' + '/'.join([self.API_VERSION, self.OBJ_TYPE, endpoint])
        raise NotImplementedError     

class Users(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='users')

class Studies(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='studies')

class Companies(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='companies')

class Interactions(BaseObjects):
    def __init__(self, credential):
        super().__init__(credential, obj_type='interactions')