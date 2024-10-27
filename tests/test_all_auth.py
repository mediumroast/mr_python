import unittest
import os
import base64
import hashlib
import json
from unittest.mock import patch, MagicMock
from mediumroast_py.api.authorize import GitHubAuth
from mediumroast_py.api.github import GitHubFunctions
from pprint import pprint


class TestMediumroastForGitHubAuth(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global separator
        separator = '-' * 50

        global test_separator
        test_separator = '=' * 50

        global process_name
        process_name = 'mediumroast_py_unit_tests'

        print('Test setup complete, starting tests.')
        print(test_separator)

    def test_pem_auth(self):
        print('Test GitHubAuth: get_access_token_pem')
        print(separator)

        token_info = {}

        auth = GitHubAuth(env={
            'clientId': os.getenv('MR_CLIENT_ID'), 
            'appId': os.getenv('MR_APP_ID'),
            'installationId': os.getenv('YOUR_INSTALLATION_ID'),
            'secretFile': os.getenv('YOUR_PEM_FILE')
        })

        token_info = auth.get_access_token_pem()
        self.assertTrue('token' in token_info and token_info['token'], "Token should be present and not empty.")
        print(f"Access token from pem authorization: {token_info['token']}")

        print(separator)

        example_response = {
            'login': 'mediumroast',
        }

        print('Test for token validity using GitHubFunctions using pem get_github_org')
        functions = GitHubFunctions(token_info['token'], os.getenv('YOUR_ORG'), process_name)
        org_info = functions.get_github_org()
        print(f"Expected org:  {example_response['login']}")
        print(f"Resulting org: {org_info[1]['login']}")
        self.assertEqual(org_info[1]['login'], example_response['login'])
        print(separator)

        print('Test GitHubAuth using pem: check_and_refresh_token')
        print(separator)

        token_info = auth.check_and_refresh_token(token_info, force_refresh=True)
        print(f"Refreshed access token from pem authorization: {token_info['token']}")
        print(separator)

        print('Retest for token validity using GitHubFunctions using pem: get_github_org')
        functions = GitHubFunctions(token_info['token'], os.getenv('YOUR_ORG'), process_name)
        org_info = functions.get_github_org()
        print(f"Expected org:  {example_response['login']}")
        print(f"Resulting org: {org_info[1]['login']}")
        self.assertEqual(org_info[1]['login'], example_response['login'])
        print(test_separator)
        
        
    def test_pat_auth(self):
        print('Test GitHubAuth: get_access_token_pat')
        print(separator)

        token_info = {}

        auth = GitHubAuth(env={
            'clientId': os.getenv('MR_CLIENT_ID'), 
            'appId': os.getenv('MR_APP_ID'),
            'installationId': os.getenv('YOUR_INSTALLATION_ID'),
            'secretFile': os.getenv('YOUR_PAT_FILE')
        })

        # Check for token validity
        token = str()
        with open(os.getenv('YOUR_PAT_FILE'), 'r') as f:
            token = f.read()
            is_valid = auth.check_token_expiration(token)
            self.assertTrue(is_valid[0], f"Token should be valid, result is {is_valid[2]}.")
            print(separator)

        token_info = auth.get_access_token_pat()
        self.assertTrue('token' in token_info and token_info['token'], "Token should be present and not empty.")
        print(f"Access token from pat authorization: {token_info['token']}")

        print(separator)

        example_response = {
            'login': 'mediumroast',
        }

        print('Test for token validity using GitHubFunctions using pat: get_github_org')
        functions = GitHubFunctions(token_info['token'], os.getenv('YOUR_ORG'), process_name)
        org_info = functions.get_github_org()
        print(f"Expected org:  {example_response['login']}")
        print(f"Resulting org: {org_info[1]['login']}")
        self.assertEqual(org_info[1]['login'], example_response['login'])
        print(separator)


    def test_device_flow_auth(self):
        print('Test GitHubAuth: get_access_token_device_flow')
        print(separator)

        token_info = {}

        auth = GitHubAuth(env={
            'clientId': os.getenv('MR_CLIENT_ID'), 
        })

        token_info = auth.get_access_token_device_flow()
        self.assertTrue('token' in token_info and token_info['token'], "Token should be present and not empty.")
        print(f"Access token from device flow authorization: {token_info['token']}")

        print(separator)

        example_response = {
            'login': 'mediumroast',
        }

        print('Test for token validity using GitHubFunctions using device flow get_github_org')
        functions = GitHubFunctions(token_info['token'], os.getenv('YOUR_ORG'), process_name)
        org_info = functions.get_github_org()
        print(f"Expected org:  {example_response['login']}")
        print(f"Resulting org: {org_info[1]['login']}")
        self.assertEqual(org_info[1]['login'], example_response['login'])
        print(separator)

        print('Test GitHubAuth using device flow: check_and_refresh_token')
        print(separator)

        token_info = auth.check_and_refresh_token(token_info, force_refresh=True)
        print(f"Refreshed access token from device flow authorization: {token_info['token']}")
        print(separator)

        print('Retest for token validity using GitHubFunctions using device flow: get_github_org')
        functions = GitHubFunctions(token_info['token'], os.getenv('YOUR_ORG'), process_name)
        org_info = functions.get_github_org()
        print(f"Expected org:  {example_response['login']}")
        print(f"Resulting org: {org_info[1]['login']}")
        self.assertEqual(org_info[1]['login'], example_response['login'])
        print(test_separator)





if __name__ == '__main__':
    unittest.main()