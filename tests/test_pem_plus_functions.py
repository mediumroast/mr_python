import unittest
import os
import base64
import hashlib
from unittest.mock import patch, MagicMock
from mediumroast_py.api.authorize import GitHubAuth
from mediumroast_py.api.github import GitHubFunctions
from mediumroast_py.api.github_server import Companies, Interactions
from pprint import pprint


class TestGitHubAuth(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global separator
        separator = '-' * 50

        global test_separator
        test_separator = '=' * 50

        global process_name
        process_name = 'mediumroast_py_unit_tests'

        print(test_separator)
        print('Setting pem authorization for tests...')
        global token_info
        auth = GitHubAuth(env={'clientId': os.getenv('MR_CLIENT_ID')})
        token_info = auth.get_access_token_pem(os.getenv('YOUR_PEM_FILE'), os.getenv('MR_APP_ID'), os.getenv('YOUR_INSTALLATION_ID'))
        print(f"Access token from pem authorization: {token_info['token']}")
        
        print('Test setup complete, starting tests.')
        print(test_separator)

    @patch('requests.post')
    def test_get_github_org(self, mock_post):
        
        print('Test GitHubFunctions: get_github_org')
        print(separator)

        example_response = {
            'login': 'mediumroast',
        }
        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = example_response
        functions = GitHubFunctions(token_info['token'], os.getenv('YOUR_ORG'), process_name)
        org_info = functions.get_github_org()
        print(f"Expected org:  {example_response['login']}")
        print(f"Resulting org: {org_info[1]['login']}")
        self.assertEqual(org_info[1]['login'], example_response['login'])
        print(test_separator)

    @patch('requests.post')
    def test_get_companies(self, mock_post):
        
        print('Test Companies: get_all')
        print(separator)

        example_response = {
            'result': True,
            'message': 'SUCCESS: read objects from container [Companies]'
        }

        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = example_response
        api_ctl = Companies(token_info['token'], os.getenv('YOUR_ORG') , process_name)
        companies = api_ctl.get_all()
        self.assertEqual(companies[0], example_response['result'])
        print('Example company:')
        pprint(companies[2][0])
        print(test_separator)

    @patch('requests.post')
    def test_get_interactions(self, mock_post):
        
        print('Test Interactions: get_all')
        print(separator)

        example_response = {
            'result': True,
            'message': 'SUCCESS: read objects from container [Interactions]'
        }

        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = example_response
        api_ctl = Interactions(token_info['token'], os.getenv('YOUR_ORG') , process_name)
        interactions = api_ctl.get_all()
        self.assertEqual(interactions[0], example_response['result'])
        print('Example Interaction:')
        global example_interaction
        example_interaction = interactions[2][0]
        pprint(example_interaction)
        print(test_separator)

    @patch('requests.post')
    def test_get_download_interaction(self, mock_post):
        
        print('Test Interactions: download_interaction_content')
        print(separator)

        
        api_ctl = Interactions(token_info['token'], os.getenv('YOUR_ORG') , process_name)
        interactions = api_ctl.get_all()
        example_interaction = interactions[2][0]
        example_response = {
            'result': True,
            'hash': example_interaction['file_hash'],
            'name': example_interaction['name'],
        }
        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = example_response
        interaction = api_ctl.download_interaction_content(example_interaction['name'])
        self.assertEqual(interaction[0], example_response['result'])

        # Compute the SHA265 hash of the downloaded file which is in interaction[2]
        sha256_hash = hashlib.sha256()
        # Since the file was retrieved from the function download_interaction_content, it is ready to be read
        sha256_hash.update(base64.b64encode(interaction[2]))
        computed_hash = sha256_hash.hexdigest()
        # Compare the computed hash with the hash from the example interaction
        self.assertEqual(computed_hash, example_response['hash'])
        # Print expected and computed hashes
        print(f"Expected hash: {example_response['hash']}")
        print(f"Resulting hash: {computed_hash}")
        print(test_separator)



if __name__ == '__main__':
    unittest.main()