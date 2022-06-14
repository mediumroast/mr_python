#!/bin/env python3
__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."


import sys
import json

from mr_python.api.mr_server import Auth as authenticate
from mr_python.api.mr_server import Users as user
import base_cli

if __name__ == "__main__":

    # Instantiate the base CLI object
    my_cli = base_cli.MrCLI(
        name='get_users', 
        description='Example CLI utility to pull user information from the mediumroast.io backend.'
    )
    
    # Get the command line arguments, config file and then set the environment
    my_args = my_cli.get_cli_args()
    [status, message, my_config] = my_cli.get_config_file(my_args.conf_file)
    [status, message, my_env] = my_cli.set_env(my_args, my_config)

    # Perform the authentication
    auth_ctl = authenticate(
        user=my_env['user'], 
        secret=my_env['secret'], 
        rest_server=my_env['rest_server'],
        api_key=my_env['api_key'],
        server_type=my_env['server_type']
    )
    credential = auth_ctl.login()

    # Create the API controller
    api_ctl = user(credential)

    # Get all users
    [success, msg, resp] = api_ctl.get_all()

    if success:
        if my_args.pretty_output:
            my_cli.printer.pprint(resp)
        else:
            print(json.dumps(resp))

    else:
        print("CLI ERROR: This is a generic error message, as something went wrong.")
        sys.exit(-1)
