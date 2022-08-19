__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import pathlib
import pprint
import argparse
import sys
import json
import configparser as conf

# Perform local imports
from mediumroast_py.helpers import utilities

class MrCLI:
    def __init__(self, name, description) -> None:
        self.DESC = description
        self.NAME = name
        self.printer = pprint.PrettyPrinter(indent=1, compact=True)
        self.util = utilities()

        # Perform argument and environmental setup
        # TODO create some safety for failure to read the config file...
        self.args = self.get_cli_args()
        [success, msg, my_conf] = self.get_config_file(self.args.conf_file)
        [success, msg, my_env] = self.set_env(self.args, my_conf)
        self.env = my_env

    def get_cli_args(self):
        """Parse common CLI arguments including system configs and behavior switches.
        """
        # Set up the argument parser
        parser = argparse.ArgumentParser(prog=self.NAME, description=self.DESC)

        # Gather system oriented configuration variables from the command line
        parser.add_argument(
            '--conf_file',
            help="Fully qualified filename for storing the configuration variables.",
            type=str,
            dest='conf_file',
            default=str(pathlib.Path.home()) + '/.mediumroast/config.ini',
        )
        parser.add_argument(
            "--mr_backend_url",
            help="The URL of the target mediumroast.io server",
            type=str,
            dest="rest_server",
        )
        parser.add_argument(
            "--api_key",
            help="The API key needed to talk to the mediumroast.io server",
            type=str,
            dest="api_key",
        )
        parser.add_argument(
            "--user", help="User name", type=str, dest="user"
        )
        parser.add_argument(
            "--secret", help="Secret or password", type=str, dest="secret"
        )
        parser.add_argument(
            "--pretty_output",
            help="Specify if the STDOUT format is pretty printed or not",
            dest="pretty_output",
            action='store_true',
            default=True,
        )

        # Gather general function oriented switches to control the behavior of the CLI
        parser.add_argument(
            "--get_by_id", help="Get object by ID", type=str, dest="by_id"
        )
        parser.add_argument(
            "--get_by_x", help="Get object by an arbitrary attribute as specified by JSON (ex \'{\"zip_postal\":\"92131\"}\')", type=str, dest="by_x"
        )
        parser.add_argument(
            "--get_by_name", help="Get object by name", type=str, dest="by_name"
        )
        parser.add_argument(
            "--create", help="Add objects to the backend by specifying a JSON file", type=str, dest="json_obj"
        )
        parser.add_argument(
            "--update", help="Update an object from the backend by specifying the object's id and value to update in JSON", type=str, dest="update_obj"
        )
        parser.add_argument(
            "--delete", help="Delete an object from the backend by specifyin the object's id", type=str, dest="obj_id"
        )

        # Parse the CLI
        cli_args = parser.parse_args()

        # Return parsed arguments
        return cli_args

    def get_config_file(self, filename):
        """A safe wrapper around reading a INI inspired config file.
        """
        config = conf.ConfigParser()
        try:
            config.read(filename)
        except conf.Error as err:
            return False, {"status_code": "FAILED", "message": err}

        return True, {"status_code": "SUCCEEDED"}, config

    def set_env(self, cli_args, config):
        """Set up the core environment variables and return a dict with them included.

        The order of priority for the arguments is:
            1. CLI switches are the first priority and override the config file
            2. The settings in the config file are used when no CLI switches are provided

        For users the preference should be to put key and common environmental variables into
        the configuration file to reduce the need for CLI switches.
        """

        # Explicitly set the essential environment variables to None
        env = {
            'rest_server': None,
            'user': None,
            'secret': None,
            'api_key': None,
        }

        # Now set the environment up in the priority as documented above
        env['rest_server'] = cli_args.rest_server if cli_args.rest_server else config['DEFAULT']['rest_server']
        env['user'] = cli_args.user if cli_args.user else config['DEFAULT']['user']
        env['secret'] = cli_args.secret if cli_args.secret else config['DEFAULT']['secret']
        env['api_key'] = cli_args.api_key if cli_args.api_key else config['DEFAULT']['api_key']

        return True, {"status_code": "SUCCEEDED"}, env

    def run_cli(self, api_controller, object_type):
        """Execute the CLI operations as per the switches and arguments.
        """
        # Explicitly set these variables to empty strings
        [success, msg, resp] = [str, str, str]
        if self.args.json_obj:
            # Create objects from a json file
            [success, my_objs] = self.util.json_read(self.args.json_obj)
            for obj in my_objs:
                [success, msg, resp] = api_controller.create_obj(obj)
                if success:
                    print("Backend response: ", end="")
                    if self.args.pretty_output:
                        self.printer.pprint(resp)
                    else:
                        print(json.dumps(resp))
                else:
                    print('An error occured: ', msg)
                    sys.exit(-1)
            print('Successfully created [' + str(self.util.total_item(my_objs)) + '] ' + object_type + ' object(s), exiting.')
            sys.exit(0)
        elif self.args.update_obj:
            # Create objects from a json file
            my_obj = json.loads(self.args.update_obj)
            [success, msg, resp] = api_controller.update_obj(my_obj)
            if success:
                print("Backend response: ", end="")
                if self.args.pretty_output:
                    self.printer.pprint(resp)
                else:
                    print(json.dumps(resp))
            else:
                    print('CLI Error: ', msg)
                    sys.exit(-1)
            print('Successfully updated ' + object_type + ' object with id [' + str(my_obj['id']) + '] exiting.')
            sys.exit(0)
        elif self.args.by_name:
            # Get a single user by name
            [success, msg, resp] = api_controller.get_by_name(self.args.by_name)
        elif self.args.by_id:
            # Get a single user by id
            [success, msg, resp] = api_controller.get_by_id(self.args.by_id)
        elif self.args.by_x:
            # Get a single user by an arbitrary attribute X
            my_obj = json.loads(self.args.by_x)
            attr = list(my_obj.keys())[0]
            value = list(my_obj.values())[0]
            [success, msg, resp] = api_controller.get_by_x(attr, value)
        else:
            # Get all users
            [success, msg, resp] = api_controller.get_all()

        # Print the output either in json or pretty format
        if success:
            if self.args.pretty_output:
                self.printer.pprint(resp)
            else:
                print(json.dumps(resp))

        else:
            print('CLI Error: ', msg)
            sys.exit(-1)

