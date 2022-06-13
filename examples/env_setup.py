#!/bin/env python3
__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

import sys
import getpass
import configparser as conf
from mr_python.helpers import utilities as util
import pathlib as path


if __name__ == '__main__':
    # Instantiate objects
    my_util = util()

    # Source and target configuration details
    config_file = 'config.ini'
    source_config_dir = './.mediumroast/'
    source_config_file = source_config_dir + config_file
    target_config_dir = str(path.Path.home()) + '/.mediumroast/'
    target_config_file = target_config_dir + config_file

    # House keeping to see if the config file already exists
    [status, msg] = my_util.check_file_system_object(target_config_file)
    ans = 'n'
    if status: 
        ans = input('It looks like the target configuration file [' + target_config_file + '] already exists. Overwrite [Y/n]?')
    if ans == 'n':
        print('Exiting, target configuration file wasn\'t overwritten.')
        sys.exit(0)

    # House keeping to see if the config directory exists
    [status, msg] = my_util.make_directory(target_config_dir)
    if not status:
        print(msg)
        sys.exit(-1)

    # Read the default configuration file
    config = conf.ConfigParser()
    config.read(source_config_file)

    # Defaults for environment setting
    env = {
        'rest_server': 'IP address or host name of mediumroast.io server, default [', 
        'user': 'Your mediumroast.io user name, default [',
        'secret': 'The password for your user name: ',
        'api_key': 'The API key for the mediumroast.io server: ',
        'server_type': 'Define the server type for the mediumroast.io backend, default: ',
        'working_dir': 'Specify the working directory for the CLI, default: '
    }

    # Helper strings for the rest_server
    proto = 'http://'
    port = ':6767'

    # Section for storing the environment variables
    section = 'DEFAULT'

    # Explicitly set answer to None
    answer = None

    # Process the rest_server name
    item = 'rest_server'
    answer = input(env[item] + config.get(section, item) + ']: ')
    config[section][item] = answer if answer else False

    # Process the user name
    item = 'user'
    answer = input(env[item] + config.get(section, item) + ']: ')
    config[section][item] = answer if answer else False

    # Process the user password
    item = 'secret'
    answer = getpass.getpass(env[item])
    config[section][item] = answer if answer else False

    # Process the api_key
    item = 'api_key'
    answer = getpass.getpass(env[item])
    config[section][item] = answer if answer else False

    # Process the server_type
    item = 'server_type'
    answer = input(env[item] + config.get(section, item) + ']: ')
    config[section][item] = answer if answer else False

    # Process the working_dir
    item = 'working_dir'
    answer = input(env[item] + config.get(section, item) + ']: ')
    config[section][item] = answer if answer else False