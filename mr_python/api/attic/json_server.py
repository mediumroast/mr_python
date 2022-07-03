__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

from ..helpers import utilities
import requests

class rest_scaffold:
    def __init__(self, credential):
        self.CRED=credential

    def get_obj(self, endpoint):
        url=self.CRED['rest_url'] + endpoint
        resp_obj=requests.get(url)
        return resp_obj.json()

    def put_obj(self, endpoint, obj):
        url=self.CRED['rest_url'] + endpoint
        resp_obj=requests.put(url, json=obj)
        return resp_obj.json(), resp_obj.status_code

    def patch_obj(self, endpoint, obj):
        url=self.CRED['rest_url'] + endpoint
        try: # Try to make the request
            resp_obj=requests.patch(url, json=obj)
            resp_obj.raise_for_status()
        except requests.exceptions.HTTPError as err: # If the request fails then return the error and False
            return False, {"status_code": resp_obj.status_code, "message": err}
        
        return True, resp_obj.json()


    # TODO implement study.corpus.set_state <-- should be done for parent/children
    # TODO implement company.corpus.set_state <-- should be done for parent/children




class Auth:
    def __init__(self, rest_server_url, user_name, secret, server_type="json"):
        self.REST_URL=rest_server_url
        self.SERVER_TYPE=server_type
        self.USER=user_name
        self.SECRET=secret
        self.utils=utilities()

    def login(self):
        token=self.utils.hash_it(self.USER + self.SECRET)
        return {
            "access_token": token,
            "refresh_token": token,
            "server_type": self.SERVER_TYPE,
            "user_name": self.USER,
            "rest_url": self.REST_URL
        }

    def logout(self):
        pass


class Studies:
    def __init__(self, credential):
        self.CRED=credential
        self.calls=rest_scaffold(credential)
    
    def get_all(self):
        my_url='/studies'
        return self.calls.get_obj(my_url)


    def get_guid_by_name(self, name):
        my_url='/studies?studyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'studyName': my_obj['studyName'],
            'GUID': my_obj['GUID']            
        }

    def get_name_by_guid(self, guid):
        my_url='/studies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'studyName': my_obj['studyName']
        }
    
    def get_by_name(self, name):
        my_url='/studies?studyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_by_guid(self, guid):
        my_url='/studies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_substudies(self):
        my_url='/studies'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"studyName": my_obj['studyName'],
                "GUID": my_obj['GUID'],
                "linkedCompanies": my_obj['linkedCompanies'],
                "substudies": my_obj['substudies']}
            )
        return filtered_objs

    def get_themes_by_guid(self, guid):
        my_url='/studies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        my_substudies=my_obj['substudies']
        filtered_objs={
            'GUID': my_obj['GUID'],
            'studyName': my_obj['studyName']
        }
        for substudy in my_substudies:
            filtered_objs={
                substudy: {
                    'themes': my_substudies[substudy]['keyThemes'],
                    'quotes': my_substudies[substudy]['keyThemeQuotes']
                }
            }
        return filtered_objs

    def get_unthemed_substudies(self):
        my_url='/studies'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            entry={"studyName": my_obj['studyName'],
                    "GUID": my_obj['GUID'],
                    "linkedCompanies": my_obj['linkedCompanies']}
            substudies=dict()
            for substudy in my_obj['substudies']:
                if not my_obj['substudies'][substudy]['themeState']:
                    substudies[substudy]=my_obj['substudies'][substudy]
                else: continue
            entry['substudies']=substudies
            filtered_objs.append(entry)
        return filtered_objs

    def get_substudies_by_guid(self, guid):
        my_url='/studies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'studyName': my_obj['studyName'],
            'substudies': my_obj['substudies']
        }

    def set_property(self, guid, json):
        my_url='/studies/' + guid + '/'
        my_obj, my_status=self.calls.patch_obj(my_url, json)
        return my_obj, my_status


class Companies:
    def __init__(self, credential):
        self.CRED=credential
        self.calls=rest_scaffold(credential)
    
    def get_all(self):
        my_url='/companies'
        return self.calls.get_obj(my_url)

    """def get_iterations(self):
        my_url='/companies'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"companyName": my_obj['companyName'],
                "GUID": my_obj['GUID'],
                "iterations": my_obj['iterations']}
            )
        return filtered_objs """

    def get_guid_by_name(self, name):
        my_url='/companies?companyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'companyName': my_obj['companyName'],
            'GUID': my_obj['GUID']            
        }

    def get_name_by_guid(self, guid):
        my_url='/companies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'companyName': my_obj['companyName']
        }
    
    def get_by_name(self, name):
        my_url='/companies?companyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_by_guid(self, guid):
        my_url='/companies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_iterations_by_state(self, state='unsummarized'):
        my_url='/companies?iterations.state_like=' + state
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append({"companyName": my_obj['companyName'],
                    "GUID": my_obj['GUID'],
                    "iterations": my_obj['iterations']})
        return filtered_objs

    def set_interaction_state(self, guid, state='umsummarized'):
        my_url='/companies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'companyName': my_obj['companyName'],
            'GUID': my_obj['GUID'],
            'iterations': my_obj['iterations']
        }
    
    def set_iteration_state(self, state='umsummarized'):
        pass

    def set_iteration_container_state(self, state='umsummarized'):
        pass

    def set_property(self, guid, json):
        my_url='/companies/' + guid + '/'
        my_status, my_obj=self.calls.patch_obj(my_url, json)
        return my_status, my_obj



class Interactions:
    def __init__(self, credential):
        self.CRED=credential
        self.calls=rest_scaffold(credential)
    
    def get_all(self):
        my_url='/interactions'
        return self.calls.get_obj(my_url)

    def get_all_states(self):
        my_url='/interactions'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"interactionName": my_obj['interactionName'],
                "GUID": my_obj['GUID'],
                "state": my_obj['state'],
                "abstract": my_obj['abstract'],
                "url": my_obj['url']}
            )
        return filtered_objs

    def get_all_states_dict(self):
        my_url='/interactions'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs={}
        for my_obj in my_objs:
            filtered_objs[my_obj['GUID']]={
                "interactionName": my_obj['interactionName'],
                "state": my_obj['state'],
                "url": my_obj['url']
            }
        return filtered_objs

    def get_all_unsummarized_dict(self, state='unsummarized'):
        my_url='/interactions?state=' + state
        my_objs=self.calls.get_obj(my_url)
        filtered_objs={}
        for my_obj in my_objs:
            filtered_objs[my_obj['GUID']]={
                "interactionName": my_obj['interactionName'],
                "state": my_obj['state'],
                "url": my_obj['url']
            }
        return filtered_objs
    
    def get_all_unsummarized_list(self, state='unsummarized'):
        my_url='/interactions?state=' + state
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"interactionName": my_obj['interactionName'],
                "GUID": my_obj['GUID'],
                "state": my_obj['state'],
                "abstract": my_obj['abstract'],
                "url": my_obj['url']}
            )
        return filtered_objs

    def get_guid_by_name(self, name):
        my_url='/interactions?interactionName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'interactionName': my_obj['interactionName'],
            'GUID': my_obj['GUID']            
        }

    def get_name_by_guid(self, guid):
        my_url='/interactions?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'interactionName': my_obj['interactionName']
        }

    def get_url_by_guid(self, guid):
        my_url='/interactions?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'interactionName': my_obj['interactionName'],
            'url': my_obj['url'],
        }

    def get_abs_by_guid(self, guid):
        my_url='/interactions?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'interactionName': my_obj['interactionName'],
            'abstract': my_obj['abstract'],
        }

    def get_by_name(self, name):
        my_url='/interactions?interactionName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_by_guid(self, guid):
        my_url='/interactions/?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_state_by_guid(self, guid):
        my_url='/interactions/?GUID=' + guid + '/'
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'interactionName': my_obj['interactionName'],
            'state': my_obj['state'],
        }

    def set_state(self, guid, state):
        my_url='/interactions/' + guid + '/'
        my_json={"state": state}
        my_status, my_obj=self.calls.patch_obj(my_url, my_json)
        return my_status, my_obj

    def set_summary(self, guid, summary):
        my_url='/interactions/' + guid + '/'
        my_json={"abstract": summary}
        my_status, my_obj=self.calls.patch_obj(my_url, my_json)
        return my_status, my_obj

    def set_property(self, guid, json):
        my_url='/interactions/' + guid + '/'
        my_status, my_obj=self.calls.patch_obj(my_url, json)
        return my_status, my_obj