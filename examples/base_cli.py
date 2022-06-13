__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import pathlib
import pprint
import argparse
import configparser as conf

class MrCLI:
    def __init__(self, name, description) -> None:
        self.DESC = description
        self.NAME = name
        self.printer = pprint.PrettyPrinter(indent=1, compact=True)

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
            required=True,
            default=str(pathlib.Path.home()) + '/.mediumroast/config.ini'
        )
        parser.add_argument(
            "--rest_url",
            help="The URL of the target REST server",
            type=str,
            dest="rest_url",
        )
        parser.add_argument(
            "--api_key",
            help="The API key needed to talk to the backend",
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
            default=False,
        )

        # Gather general function oriented switches to control the behavior of the CLI
        parser.add_argument(
            "--get_name_by_guid",
            help="Get study name by GUID",
            type=str,
            dest="name_by_guid",
        )
        parser.add_argument(
            "--get_guid_by_name",
            help="Get GUID by study name",
            type=str,
            dest="guid_by_name",
        )
        parser.add_argument(
            "--get_by_guid", help="Get object by GUID", type=str, dest="by_guid"
        )
        parser.add_argument(
            "--get_by_name", help="Get object by name", type=str, dest="by_name"
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
            'rest_url': None,
            'user': None,
            'secret': None,
            'api_key': None,
        }

        # Now set the environment up in the priority as documented above
        env['rest_url'] = cli_args.rest_url if cli_args.rest_url else config.get('DEFAULT', )

        pass

