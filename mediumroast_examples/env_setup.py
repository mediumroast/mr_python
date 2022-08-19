#!/bin/env python3
__version__ = '1.1'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

import sys
import getpass
import pyfiglet
import configparser as conf
from mediumroast_py.helpers import utilities as util
import pathlib as path

if __name__ == '__main__':
    # Welcome the user to the environmental setup
    intro = pyfiglet.figlet_format('Mediumroast CLI/API setup.')
    print(intro,"\n", '-'*80, "\n")

    # Instantiate objects
    my_util = util()

    # Source and target configuration details
    config_file = 'config.ini'
    source_config_dir = './.mediumroast/'
    source_config_file = source_config_dir + config_file
    target_config_dir = str(path.Path.home()) + '/.mediumroast/'
    target_config_file = target_config_dir + config_file

    # House keeping to see if the config file already exists
    print('Checking to see if the the target configuration file [' + target_config_file + '] already exists.')
    [status, msg] = my_util.check_file_system_object(target_config_file)
    ans = 'Y'
    if status: 
        ans = input('It looks like the target configuration file [' + target_config_file + '] exists. Overwrite [Y/n]? ').strip()
    if ans == 'n':
        print('Exiting, target configuration file wasn\'t overwritten.')
        sys.exit(0)
    else:
        print('Target configuration file not detected, proceeding...\n')

    # House keeping to see if the config directory exists
    [status, msg] = my_util.make_directory(target_config_dir)
    if not status:
        print(msg)
        sys.exit(-1)

    # Read the default configuration file
    config = conf.ConfigParser()
    config.read(source_config_file)

    # Environmentals and their prompt text for inputs
    env = {
        'mediumroast_server': 'IP address or host name of mediumroast.io server, default [',
        'mediumroast_port': 'TCP port used for the mediumroast.io server, default [', 
        'user': 'Your mediumroast.io user name, default [',
        'secret': 'The password for your user name: ',
        'api_key': 'The API key for the mediumroast.io server: ',
        'working_dir': 'Specify the working directory for the CLI, default ['
    }

    # Helper strings for the mediumroast_server
    proto = 'http://'

    # Section for storing the environment variables
    section = 'DEFAULT'

    # Explicitly set answer to None
    answer = None

    print('Setting up the environment for mediumroast.io...')
    # Process the rest_server name & port to create the mediumroast_server setting
    item = 'mediumroast_server'
    answer = input(env[item] + config.get(section, item) + ']: ').strip()
    mr_server = answer if answer else config[section][item]

    item = 'mediumroast_port'
    answer = input(env[item] + config.get(section, item) + ']: ').strip()
    mr_port = answer if answer else config[section][item]

    item = 'rest_server'
    config[section][item] = proto + mr_server + ':' + mr_port

    # Process the user name
    item = 'user'
    answer = input(env[item] + config.get(section, item) + ']: ').strip()
    config[section][item] = answer if answer else config[section][item]

    # Process the user password
    item = 'secret'
    answer = getpass.getpass(env[item]).strip()
    config[section][item] = answer if answer else config[section][item]

    # Process the api_key
    item = 'api_key'
    answer = getpass.getpass(env[item]).strip()
    config[section][item] = answer if answer else config[section][item]

    # Process the working_dir
    item = 'working_dir'
    answer = input(env[item] + config.get(section, item) + ']: ').strip()
    config[section][item] = answer if answer else config[section][item]

    # Verify the environment
    print("\nVerifying the current environmental settings...")
    for item in env:
        value = "[suppressed]" if (item == "secret" or item == "api_key") else config[section][item] 
        print("\t" * 2, item + " =", value)
    answer = input("Are these environmental settings correct? [Y/n] ").strip()
    if answer == "n":
        print("Ok it appears you're not ready to save these environmental settings, exiting.")
        sys.exit(0)

    # Save the environment
    print("\nSaving the current environmental settings...")
    with open(target_config_file, 'w') as configfile:
        config.write(configfile)