#!/bin/env python3
__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# mediumroast.io SDK specific imports
from mediumroast_py.api.mr_server import Auth as authenticate
from mediumroast_py.api.mr_server import Interactions as interaction
import base_cli

if __name__ == "__main__":
    #define the object type for the CLI
    object_type = 'interaction'

    # Instantiate the base CLI object
    my_cli = base_cli.MrCLI(
        name=object_type, 
        description='Example CLI utility to get and manipulate ' + object_type + 
            ' information in the mediumroast.io backend. Running without any arguments or switches will cause the default behavior of retrieving all ' + object_type + 
            ' objects.'
    )

    # Perform the authentication
    auth_ctl = authenticate(
        user=my_cli.env['user'], 
        secret=my_cli.env['secret'], 
        rest_server=my_cli.env['rest_server'],
        api_key=my_cli.env['api_key']
    )
    credential = auth_ctl.login()

    # Create the API controller
    api_ctl = interaction(credential)

    # Run the CLI
    my_cli.run_cli(api_ctl, object_type)