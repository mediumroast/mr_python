import requests
import time
import webbrowser
import jwt
from pathlib import Path
from urllib.parse import parse_qs

__license__ = "Apache 2.0"
__copyright__ = "Copyright (C) 2024 Mediumroast, Inc."
__author__ = "Michael Hay"
__email__ = "hello@mediumroast.io"
__status__ = "Production"

class GitHubAuth:
    """
    A class used to authenticate with GitHub.

    ...

    Attributes
    ----------
    env : dict
        A dictionary containing environment variables.
    client_type : str
        The type of the client ('github-app' by default).
    client_id : str
        The client ID.
    device_code : str
        The device code (None by default).

    Methods
    -------
    get_access_token_device_flow():
        Gets an access token using the device flow.
    """
    def __init__(self, env, client_type='github-app'):
        """
        Constructs all the necessary attributes for the GitHubAuth object.

        Parameters
        ----------
        env : dict
            A dictionary containing environment variables.
        client_type : str, optional
            The type of the client ('github-app' by default).
        """
        self.env = env
        self.client_type = client_type
        self.client_id = env['clientId']
        self.app_id = env['appId']
        self.installation_id = env['installationId']
        self.secret_file = env['secretFile']
        self.device_code = None

    def get_access_token_device_flow(self):
        """
        Gets an access token using the device flow.

        The method sends a POST request to 'https://github.com/login/device/code' to get the device and user codes.
        The response is expected to be a JSON object containing the device code, user code, verification URI, and the expiration time and interval for polling.

        Returns
        -------
        dict
            A dictionary containing the access token and its expiration time.
        """
        # Request device and user codes
        response = requests.post('https://github.com/login/device/code', data={
            'client_id': self.client_id
        })
        response.raise_for_status()
        data = parse_qs(response.content.decode())

        # Open the verification URL in the user's browser
        print(f"Opening browser with: {data['verification_uri'][0]}")
        webbrowser.open(data['verification_uri'][0])
        print(f"Enter the user code: {data['user_code'][0]}")
        input("Press Enter after you have input the code to continue.")

        # Poll for the access token
        while True:
            response = requests.post('https://github.com/login/oauth/access_token', data={
                'client_id': self.client_id,
                'device_code': data['device_code'][0],
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
            })
            response.raise_for_status()
            token_data = parse_qs(response.content.decode())

            if 'access_token' in token_data:
                # Assume the token expires in 1 hour
                expires_at = time.time() + int(token_data['expires_in'][0])
                return {
                    'token': token_data['access_token'][0], 
                    'refresh_token': token_data['refresh_token'][0],
                    'expires_at': expires_at, 
                    'auth_type': 'device-flow'
                }
            elif 'error' in token_data and token_data['error'][0] == 'authorization_pending':
                time.sleep(data['interval'][0])
            else:
                raise Exception(f"Failed to get access token: {token_data}")

    def get_access_token_pat(self, pat_file_path):
        """
        Get the Personal Access Token (PAT) from a file.

        Parameters
        ----------
        pat_file_path : str
            The path to the file containing the PAT.

        Returns
        -------
        str
            The PAT.
        """
        return [False, f'initial implementation completed but unconfirmed, untested and unsupported', None]
        with open(pat_file_path, 'r') as file:
            pat = file.read().strip()
        # Set the expiration time to a far future date
        expires_at = float('inf')

        return {'token': pat, 'expires_at': expires_at, 'auth_type': 'pat'}

    def get_access_token_pem(self):
        """
        Get an installation access token using a PEM file.

        Returns
        -------
        str
            The installation access token.
        """
        # Load the private key
        private_key = Path(self.secret_file).read_text()

        # Generate the JWT
        payload = {
            # issued at time
            'iat': int(time.time()),
            # JWT expiration time (10 minute maximum)
            'exp': int(time.time()) + (10 * 60),
            # GitHub App's identifier
            'iss': self.app_id
        }
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

        # Create the headers to include in the request
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Make the request to generate the installation access token
        response = requests.post(
            f'https://api.github.com/app/installations/{self.installation_id}/access_tokens', headers=headers)
        response.raise_for_status()

        # Extract the token and its expiration time from the response
        token_data = response.json()
        token = token_data['token']
        expires_at = token_data['expires_at']

        return {'token': token, 'expires_at': expires_at, 'auth_type': 'pem'}
    

    def get_access_token_client_secret(self, client_id, client_secret):
        """
        Get an access token using a client secret.

        Parameters
        ----------
        client_secret : str
            The client secret.
        client_id : str
            The client ID.

        Returns
        -------
        dict
            A dictionary containing the access token and its expiration time.
        """
        return [False, f'initial implementation completed but unconfirmed, untested and unsupported', None]
        # The URL of the token endpoint
        url = "https://github.com/login/oauth/access_token"

        # The data to send in the POST request
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": "authorization_code",  # Replace with your actual authorization code
        }

        # Make the POST request
        response = requests.post(url, data=data)

        # Check the response
        if response.status_code == 200:
            # Parse the response as JSON
            token_info = response.json()

            # Return the access token and its expiration time
            return {
                "access_token": token_info["access_token"],
                "expires_in": token_info["expires_in"],
            }
        else:
            # If the request failed, raise an exception
            response.raise_for_status()

    def check_and_refresh_token(self, token_info):
        """
        Check the expiration of the access token and regenerate it if necessary.

        Parameters
        ----------
        token_info : dict
            A dictionary containing the access token, its expiration time, and the auth type.

        Returns
        -------
        dict
            A dictionary containing the (possibly refreshed) access token, its expiration time, and the auth type.
        """
        # Check if the token has expired
        if time.time() >= token_info['expires_at']:
            # The token has expired, regenerate it
            if token_info['auth_type'] == 'pem':
                token_info = self.get_access_token_pem(self.pem_file_path, self.app_id, self.installation_id)
            elif token_info['auth_type'] == 'device_flow':
                token_info = self.get_access_token_device_flow()
            elif token_info['auth_type'] == 'pat':
                token_info = self.get_access_token_pat(self.pat_file_path)
            else:
                raise ValueError(f"Unknown auth type: {token_info['auth_type']}")

        return token_info
    
