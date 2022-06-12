__version__ = '2.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Imports for the json_server backend
from mr_python.helpers import utilities
from .json_server import Auth as json_auth
from .json_server import Companies as json_companies
from .json_server import Studies as json_studies
from .json_server import Interactions as json_interactions

# Imports for the mr_server backend
from .mr_server import Auth as mr_auth
from .mr_server import Users as mr_users


class Auth:
    """Call the login and logout functions for the underlying implementation in use.

    NOTE: In general the logout function isn't implemented at this time.
    """
    def __init__(self, rest_server_url, user_name=None, secret=None, api_key=None, server_type="mr"):
        self.REST_URL = rest_server_url
        self.SERVER_TYPE = server_type
        self.USER = user_name
        self.SECRET = secret
        self.API_KEY = api_key

    def login(self):
        if self.SERVER_TYPE == "json":
            auth = json_auth(
                rest_server_url=self.REST_URL, user_name=self.USER, secret=self.SECRET
            )
            return auth.login()
        elif self.SERVER_TYPE == 'mr':
            auth = mr_auth(
                rest_server_url=self.REST_URL, user_name=self.USER, secret=self.SECRET, 
                api_key=self.API_KEY
            )
        else:
            return NotImplementedError

    def logout(self):
        pass

class BaseObjects:
    def __init__(self, credential) -> None:
        self.CRED = credential
        self.util = utilities()

    def get_all(self, rest, endpoint):
        return rest.get_all(endpoint=endpoint)

class Users(BaseObjects):
    def __init__(self, credential) -> None:
        super().__init__(credential)
        #self.rest = mr_users(credential) if self.CRED['server_type'] == 'mr' else json_users(credential)
        self.rest = mr_users(credential)

    def get_all(self, endpoint):
        return super().get_all(self.rest, endpoint)


class Studies:
    def __init__(self, credential):
        self.CRED = credential
        self.studies = json_studies(credential)

    def get_all(self):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_all()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_guid_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_guid_by_name(name)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_name_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_name_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_by_name(name)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_substudies(self):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_substudies()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_unthemed_substudies(self):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_unthemed_substudies()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_themes(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_themes_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def set_property(self, guid, json):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.set_property(guid, json)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError


class Companies:
    def __init__(self, credential):
        self.CRED = credential
        self.companies = json_companies(credential)

    def get_all(self):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_all()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_guid_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_guid_by_name(name)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_name_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_name_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_by_name(name)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_by_guid(guid)
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    """ def get_iterations(self):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_iterations()
        else:
            #The official mr_backend implementation of this would go here
            raise NotImplementedError

    def get_iterations_by_state(self, state="unthemed"):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_iterations_by_state(state)
        else:
            #The official mr_backend implementation of this would go here
            raise NotImplementedError """

    def set_property(self, guid, json):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.set_property(guid, json)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def set_interactions_state(self, guid, state='unsummarized'):
        if self.CRED['server_type'] == 'json':
            interactions_ctl = Interactions()
            all_interactions = interactions_ctl.get_all_unsummarized()
            all_iterations = self.companies.get_iterations_by_state()
            return True, self.companies.set_interaction_state(guid, state)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    # TODO need to implement this function it is not yet coded

    def set_states_by_guid(self, guid, json):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.set_property(guid, json)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError


class Interactions:
    def __init__(self, credential):
        self.CRED = credential
        self.interactions = json_interactions(credential)

    def get_all(self):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_all()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_all_unsummarized(self):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_all_unsummarized_list()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_all_states_dict(self):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_all_states_dict()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_all_unsummarized_dict(self):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_all_unsummarized_dict()
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_guid_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_guid_by_name(name)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_name_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_name_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_url_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_url_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_abs_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_abs_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_by_name(name)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def get_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_by_guid(guid)
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def set_state(self, guid, state):
        # TODO Change to try except structure to bettle handle errors
        if self.CRED['server_type'] == 'json':
            my_status, my_obj = self.interactions.set_state(guid, state)
            return my_status, my_obj
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def set_all_states(self, state):
        if self.CRED['server_type'] == 'json':
            final_objs = []
            interactions = self.interactions.get_all_states()
            for interaction in interactions:
                prev_state = interaction['state']
                if state == prev_state:
                    continue  # Skip if this is already at desired state
                my_status, my_obj = self.set_state(interaction['GUID'], state)
                if not my_status:
                    return my_status, my_obj  # Oops there was an error in the request and we need to bale
                final_objs.append({
                    "interactionName": interaction['interactionName'],
                    'GUID': my_obj['id'],
                    'state': my_obj['state'],
                    'previous state': prev_state
                })
            return True, final_objs
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def del_all_abstracts(self):
        if self.CRED['server_type'] == 'json':
            final_objs = []
            interactions = self.interactions.get_all_states()
            for interaction in interactions:
                my_status, my_obj = self.set_summary(
                    interaction['GUID'], 'Unknown')
                if not my_status:
                    return my_status, my_obj  # Oops there was an error in the request and we need to bale
                my_status, my_obj = self.set_state(
                    interaction['GUID'], 'unsummarized')
                if not my_status:
                    return my_status, my_obj  # Oops there was an error in the request and we need to bale
                final_objs.append({
                    "interactionName": interaction['interactionName'],
                    'GUID': my_obj['id'],
                    'state': my_obj['state'],
                    'abstract': my_obj['abstract']
                })
            return True, final_objs
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def set_summary(self, guid, summary):
        if self.CRED['server_type'] == 'json':
            my_status, my_obj = self.interactions.set_summary(guid, summary)
            return my_status, my_obj
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError

    def set_property(self, guid, json):
        if self.CRED['server_type'] == 'json':
            my_status, my_obj = self.interactions.set_property(guid, json)
            return my_status, my_obj
        else:
            """The official mr_backend implementation of this would go here"""
            raise NotImplementedError
