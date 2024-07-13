import requests
from datetime import datetime, timezone, timedelta
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
        self.app_id = env['appId'] if 'appId' in env else None
        self.installation_id = env['installationId'] if 'installationId' in env else None
        self.secret_file = env['secretFile']  if 'secretFile' in env else None
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
                expiration_time = datetime.now(timezone.utc) + timedelta(seconds=3600)
                expires_at = expiration_time.strftime("%Y-%m-%dT%H:%M:%SZ")
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

    def get_access_token_pat(self, default_expiry_days=30):
        """
        Get the Personal Access Token (PAT) from a file.

        Parameters
        ----------
        pat_file_path : str
            The path to the file containing the PAT.
        default_expiry_days : int, optional
            The default number of days until the PAT expires (30 by default).

        Returns
        -------
        str
            The PAT.
        """
        with open(self.secret_file, 'r') as file:
            pat = file.read().strip()
        # Set the expiration time to a far future date
        expiration_date = datetime.now(timezone.utc) + timedelta(days=default_expiry_days)
        expires_at = expiration_date.strftime("%Y-%m-%dT%H:%M:%SZ")

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
    

    def check_and_refresh_token(self, token_info, force_refresh=False):
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
        expiry = datetime.strptime(token_info['expires_at'], "%Y-%m-%dT%H:%M:%SZ")
        expiry = expiry.replace(tzinfo=timezone.utc)
        # Check if the token has expired
        if datetime.now(timezone.utc) < expiry or force_refresh:
            # The token has expired, regenerate it
            if token_info['auth_type'] == 'pem':
                token_info = self.get_access_token_pem()
            elif token_info['auth_type'] == 'device-flow':
                token_info = self.get_access_token_device_flow()
            elif token_info['auth_type'] == 'pat':
                raise ValueError("Automatic PAT refresh is not supported. Please generate a new PAT.")
            else:
                raise ValueError(f"Unknown auth type: {token_info['auth_type']}")

        return token_info
    
