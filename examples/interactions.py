#!/bin/env python3
__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Python standard library imports
import sys
import json

# mediumroast.io SDK specific imports
from mr_python.api.mr_server import Auth as authenticate
from mr_python.api.mr_server import Interactions as interaction
from mr_python.helpers import utilities as util
import base_cli

if __name__ == "__main__":

    # Instantiate the base CLI object
    my_cli = base_cli.MrCLI(
        name='interactions', 
        description='Example CLI utility to get and manipulate interaction information in the mediumroast.io backend.'
    )
    
    # Get the command line arguments, config file and then set the environment
    my_args = my_cli.get_cli_args()
    [success, msg, my_config] = my_cli.get_config_file(my_args.conf_file)
    [success, msg, my_env] = my_cli.set_env(my_args, my_config)

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
    api_ctl = interaction(credential)

    # Explicitly set these variables to empty strings
    [success, msg, resp] = [str, str, str]
    if my_args.json_obj:
        # Create objects from a json file
        my_objs = util.json_read(file_name=my_args.json_obj)
        for obj in my_objs:
            [success, msg, resp] = api_ctl.create_obj(obj)
            if success:
                if my_args.pretty_output:
                    my_cli.printer.pprint(resp)
                else:
                    print(json.dumps(resp))
        print('Successfully created [' + str(util.total_item(my_objs)) + '] interaction objects, exiting.')
        sys.exit(0)
    elif my_args.by_name:
        # Get a single user by name
        [success, msg, resp] = api_ctl.get_by_name(my_args.by_name)
    elif my_args.by_id:
        # Get a single user by id
        [success, msg, resp] = api_ctl.get_by_id(my_args.by_id)
    else:
        # Get all users
        [success, msg, resp] = api_ctl.get_all()

    # Print the output either in json or pretty format
    if success:
        if my_args.pretty_output:
            my_cli.printer.pprint(resp)
        else:
            print(json.dumps(resp))

    else:
        print("CLI ERROR: This is a generic error message, as something went wrong.")
        sys.exit(-1)

    # Explicitly logout and exit
    auth_ctl.logout()
    sys.exit(0)