import unittest
from unittest.mock import patch, MagicMock
from mediumroast_py.api.authorize import GitHubAuth
from mediumroast_py.api.github import GitHubFunctions


class TestGitHubAuth(unittest.TestCase):
    def setUp(self):
        global separator
        separator = '-' * 50

        global test_separator
        test_separator = '=' * 50

        print(test_separator)
        print('Setting pem authorization for tests...')
        global token_info
        auth = GitHubAuth(env={'clientId': 'Iv1.f5c0a4eb1f0606f8'})
        token_info = auth.get_access_token_pem('secrets/mediumroast-for-github.2024-04-18.private-key.pem', '650476', '48287264')
        print(f"Access token from pem authorization: {token_info['token']}")
        
        print('Test setup complete, starting tests.')
        print(test_separator)

    @patch('requests.post')
    def test_get_github_org(self, mock_post):
        
        print('Test GitHubFunctions: get_github_org')
        print(separator)

        example_response = {
            'login': 'mediumroast',
            'id': 48287264,
            'url': 'https://api.github.com/orgs/mediumroast'
        }
        mock_post.return_value = MagicMock()
        mock_post.return_value.json.return_value = example_response
        functions = GitHubFunctions(token_info['token'], 'mediumroast', 'mediumroast_py_unit_tests')
        org_info = functions.get_github_org()
        print(f"Org response name: {org_info[1]['login']}")
        print(f"Org example name: {example_response['login']}")
        self.assertEqual(org_info[1]['login'], example_response['login'])
        print(test_separator)

if __name__ == '__main__':
    unittest.main()