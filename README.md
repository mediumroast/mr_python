# mediumroast_py

## Introduction

This Python package provides a Software Development Kit (SDK) for interacting with Mediumroast for GitHub. It is used internally by Mediumroast, Inc. and meant for developers to make use of.

### Notice
The SDK is in active development and is subject to change. The SDK is not yet stable and should not be used in production environments. 

## Installation

To install the package, you can use pip:

```bash
pip install mediumroast_py
```

## Usage
To use the package, you will need to import the `mediumroast_py` modules and classes. The package provides three main classes for interacting with objects: `Companies`, `Interactions`, and `Users`.

### Authentication
To use the package, you will need to authenticate with the Mediumroast API using the `GitHubAuth` class. Here is an example of how to authenticate with the Mediumroast API using a GitHub App installation and a private key file. You will need to set the `MR_CLIENT_ID`, `MR_APP_ID`, and `YOUR_INSTALLATION_ID` environment variables to the appropriate values for your GitHub App installation. You will also need to set the `YOUR_PEM_FILE` environment variable to the path of your private key file. Here is an example of how to authenticate with the Mediumroast API using a GitHub App installation and a private key file.

```python
from mediumroast_py.api import Companies, Interactions, Users
from mediumroast_py.api.authorize import GitHubAuth

auth = GitHubAuth(env={'clientId': os.getenv('MR_CLIENT_ID')})
token = auth.get_access_token_pem(
      os.getenv('YOUR_PEM_FILE'), 
      os.getenv('MR_APP_ID'), 
      os.getenv('YOUR_INSTALLATION_ID')
)
```

### Companies
The `Companies` class provides methods for interacting with companies in Mediumroast. You can use the `get_all` method to get information about all companies.

```python
company_ctl = Companies(token_info['token'], os.getenv('YOUR_ORG') , process_name)
companies = company_ctl.get_all()
```

### Interactions
The `Interactions` class provides methods for interacting with interactions in Mediumroast. You can use the `get_all` method to get information about all interactions.

```python
interaction_ctl = Interactions(token_info['token'], os.getenv('YOUR_ORG') , process_name)
interactions = interaction_ctl.get_all()
```

## Issues
If you encounter any issues with the SDK, please report them on the [mediumroast_py issues](https://github.com/mediumroast/mediumroast_py/issues) page.
