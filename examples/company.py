#!/bin/env python3
__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# mediumroast.io SDK specific imports
from mr_python.api.mr_server import Auth as authenticate
from mr_python.api.mr_server import Companies as company
import base_cli

if __name__ == "__main__":
    #define the object type for the CLI
    object_type = 'company'

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
        api_key=my_cli.env['api_key'],
        server_type=my_cli.env['server_type']
    )
    credential = auth_ctl.login()

    # Create the API controller
    api_ctl = company(credential)

    # Run the CLI
    my_cli.run_cli(api_ctl, object_type)

# TODO the below is deprecated remove in a future version on the cleanup branch
# if __name__ == "__main__":

#     # Instantiate the base CLI object
#     my_cli = base_cli.MrCLI(
#         name='companies', 
#         description='Example CLI utility to get and manipulate company information in the mediumroast.io backend.'
#     )
#     util = utilities()
    
#     # Get the command line arguments, config file and then set the environment
#     my_args = my_cli.get_cli_args()
#     [success, msg, my_config] = my_cli.get_config_file(my_args.conf_file)
#     [success, msg, my_env] = my_cli.set_env(my_args, my_config)

#     # Perform the authentication
#     auth_ctl = authenticate(
#         user=my_env['user'], 
#         secret=my_env['secret'], 
#         rest_server=my_env['rest_server'],
#         api_key=my_env['api_key'],
#         server_type=my_env['server_type']
#     )
#     credential = auth_ctl.login()

#     # Create the API controller
#     api_ctl = company(credential)

#     # Explicitly set these variables to empty strings
#     [success, msg, resp] = [str, str, str]
#     if my_args.json_obj:
#         # Create objects from a json file
#         [success, my_objs] = util.json_read(my_args.json_obj)
#         for obj in my_objs:
#             [success, msg, resp] = api_ctl.create_obj(obj)
#             if success:
#                 if my_args.pretty_output:
#                     my_cli.printer.pprint(resp)
#                 else:
#                     print(json.dumps(resp))
#             else:
#                 print('An error occured: ', msg)
#                 sys.exit(-1)
#         print('Successfully created [' + str(util.total_item(my_objs)) + '] company objects, exiting.')
#         sys.exit(0)
#     elif my_args.update_obj:
#         # Create objects from a json file
#         my_obj = json.loads(my_args.update_obj)
#         [success, msg, resp] = api_ctl.update_obj(my_obj)
#         if success:
#             if my_args.pretty_output:
#                 my_cli.printer.pprint(resp)
#             else:
#                 print(json.dumps(resp))
#         else:
#                 print('CLI Error: ', msg)
#                 sys.exit(-1)
#         print('Successfully updated [' + my_obj['id'] + '] company objects, exiting.')
#         sys.exit(0)
#     elif my_args.by_name:
#         # Get a single user by name
#         [success, msg, resp] = api_ctl.get_by_name(my_args.by_name)
#     elif my_args.by_id:
#         # Get a single user by id
#         [success, msg, resp] = api_ctl.get_by_id(my_args.by_id)
#     elif my_args.by_x:
#         # Get a single user by an arbitrary attribute X
#         my_obj = json.loads(my_args.by_x)
#         attr = list(my_obj.keys())[0]
#         value = list(my_obj.values())[0]
#         [success, msg, resp] = api_ctl.get_by_x(attr, value)
#     else:
#         # Get all users
#         [success, msg, resp] = api_ctl.get_all()

#     # Print the output either in json or pretty format
#     if success:
#         if my_args.pretty_output:
#             my_cli.printer.pprint(resp)
#         else:
#             print(json.dumps(resp))

#     else:
#         print('CLI Error: ', msg)
#         sys.exit(-1)

#     # Explicitly logout and exit
#     auth_ctl.logout()
#     sys.exit(0)