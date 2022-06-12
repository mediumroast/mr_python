__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 mediumroast.io. All rights reserved."

import requests

class mr_rest:
    """Simple and safe wrappers around Python requests to make RESTful API calls simpler.

    The credential object, passed when this object is created, should includ all relevant items
    needed to authenticate a client.  This can include appropriate JWT tokens, user identifiers,
    passwords, etc.  At a minimum the rest_url is needed for a json_server backend, but when there
    is a mr_server backend then both rest_url and an api_key are needed to connect.
    """

    def __init__(self, credential):
        """Instantiate the rest_scaffold with the appropriate credential information.
        """
        self.CRED = credential

    def get_obj(self, endpoint):
        """Get an object using endpoint only.

        If the request succeeds a boolean status of True, the status code and the JSON is returned.
        Otherwise, if the request fails a boolean status of False, the status code and status message is returned.
        """
        # Extract key items from the credential and extend with endpoint
        server_type = self.CRED['server_type']
        url = self.CRED['rest_url'] + endpoint
        api_key = self.CRED['api_key']

        # Try to make the request
        try:
            # Detect if the backend server type is either a mr_server or json_server  
            resp_obj = requests.get(url, headers={'Authorization': api_key}) if server_type == "mr" else requests.put(url)
            resp_obj.raise_for_status()

        # If the request fails then return the error and False
        except requests.exceptions.HTTPError as err:  
            return False, {"status_code": resp_obj.status_code, "message": err}
        
        # Return True, status code and resulting json
        return True, {"status_code": resp_obj.status_code}, resp_obj.json()

    def put_obj(self, endpoint, obj):
        """Put an object using endpoint and a pythonic object.

        If the request succeeds a boolean status of True, the status code and the JSON is returned.
        Otherwise, if the request fails a boolean status of False, the status code and status message is returned.
        """
        # Extract key items from the credential and extend with endpoint
        server_type = self.CRED['server_type']
        url = self.CRED['rest_url'] + endpoint
        api_key = self.CRED['api_key']

        # Try to make the request
        try:  
            # Detect if the backend server type is either a mr_server or json_server
            resp_obj = requests.put(url, headers={'Authorization': api_key}, json=obj) if server_type == "mr" else requests.put(url, json=obj)
            resp_obj.raise_for_status()

        # If the request fails then return the error and False
        except requests.exceptions.HTTPError as err:  
            return False, {"status_code": resp_obj.status_code, "message": err}
        
        # Return True, status code and resulting json
        return True, {"status_code": resp_obj.status_code}, resp_obj.json()

    def patch_obj(self, endpoint, obj):
        """Patch an object using endpoint and a pythonic object.

        If the request succeeds a boolean status of True, the status code and the JSON is returned.
        Otherwise, if the request fails a boolean status of False, the status code and status message is returned.
        """
        # Extract key items from the credential and extend with endpoint
        server_type = self.CRED['server_type']
        url = self.CRED['rest_url'] + endpoint
        api_key = self.CRED['api_key']

        # Try to make the request
        try:  
            resp_obj = requests.patch(url, headers={'Authorization': api_key}, json=obj) if server_type == "mr" else requests.patch(url, json=obj)
            resp_obj.raise_for_status()

        # If the request fails then return the error and False
        except requests.exceptions.HTTPError as err:  # If the request fails then return the error and False
            return False, {"status_code": resp_obj.status_code, "message": err}
        
        # Return True, status code and resulting json
        return True, {"status_code": resp_obj.status_code}, resp_obj.json()

    def delete_obj(self, endpoint, obj):
        """Delete an object using endpoint and a pythonic object.

        If the request succeeds a boolean status of True, the status code and the JSON is returned.
        Otherwise, if the request fails a boolean status of False, the status code and status message is returned.

        WARNING: Do not user as this method hasn't been tested or validated it is here for completeness only at this time.
        """
        # Extract key items from the credential and extend with endpoint
        server_type = self.CRED['server_type']
        url = self.CRED['rest_url'] + endpoint
        api_key = self.CRED['api_key']

        # Try to make the request
        try:  
            resp_obj = requests.delete(url, headers={'Authorization': api_key}, json=obj) if server_type == "mr" else requests.delete(url, json=obj)
            resp_obj.raise_for_status()

        # If the request fails then return the error and False
        except requests.exceptions.HTTPError as err:  # If the request fails then return the error and False
            return False, {"status_code": resp_obj.status_code, "message": err}
        
        # Return True, status code and resulting json
        return True, {"status_code": resp_obj.status_code}, resp_obj.json()
