import unittest
import os
import base64
import hashlib
import json
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
        auth = GitHubAuth(env={
            'clientId': os.getenv('MR_CLIENT_ID'), 
            'appId': os.getenv('MR_APP_ID'),
            'installationId': os.getenv('YOUR_INSTALLATION_ID'),
            'secretFile': os.getenv('YOUR_PEM_FILE')
        })
        token_info = auth.get_access_token_pem()
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
        interaction = api_ctl.download_interaction_content(example_interaction['url'])
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

    @patch('requests.post')
    def test_update_interaction(self, mock_post):
        
        print('Test Interactions: update_interaction')
        print(separator)

        api_ctl = Interactions(token_info['token'], os.getenv('YOUR_ORG') , process_name)

        # Read in updated interaction content from example_data/*.json
        updates = [
            './tests/example_data/confluence_vs_sharepoint_metadata_update.json', 
            './tests/example_data/team_q1_2024_shareholder_letter_metadata_update.json'
        ]

        # Read in the updated interaction content into an array of dictionaries
        updated_content = []
        for update in updates:
            with open(update, 'r') as f:
                # Append the content of the file to the updated_content array as a dictionary using json.loads
                updated_content.append(json.loads(f.read()))

        # Modify each dictionary to include only name, status, abstract, description and topics properties and delete the other properties
        for content in updated_content:
            for key in list(content.keys()):
                if key not in ['name', 'status', 'abstract', 'description', 'topics', 'file_size', 'reading_time', 'page_count', 'content_type', 'word_count', 'contact_name']:
                    del content[key]

        # Update each interaction with the updated content
        for content in updated_content:
            # Set the interaction name to the name of the interaction to update
            interaction_name = content['name']
            # Delete the name property from the content dictionary
            del content['name']
            # Create the content dictionary to send to the update_obj function
            content = {'name': interaction_name, 'updates': content}
            example_response = {
                'result': True,
                'message': 'SUCCESS: updated object in container [Interactions]'
            }
            mock_post.return_value = MagicMock()
            mock_post.return_value.json.return_value = example_response
            update = api_ctl.update_obj(content)
            print(update)
            self.assertEqual(update[0], example_response['result'])
            print('Checking to see if sample interaction was upated ...')
            interaction_to_check = updated_content[0]['name']
            expected_status = updated_content[0]['status']
            expected_description = updated_content[0]['description']
            expected_abstract = updated_content[0]['abstract']

            # Get the interaction that was updated
            updated_interaction = api_ctl.find_by_name(interaction_to_check)
            print(f"Interaction to check: {interaction_to_check}")
            self.assertEqual(updated_interaction[0]['status'], expected_status)
            print(f"Expected status: {expected_status}")
            print(f"Resulting status: {updated_interaction[0]['status']}")
            self.assertEqual(updated_interaction[0]['description'], expected_description)
            print(f"Expected description: {expected_description}")
            print(f"Resulting description: {updated_interaction[0]['description']}")
            self.assertEqual(updated_interaction[0]['abstract'], expected_abstract)
            print(f"Expected abstract: {expected_abstract}")
            print(f"Resulting abstract: {updated_interaction[0]['abstract']}")
            print(test_separator)





if __name__ == '__main__':
    unittest.main()