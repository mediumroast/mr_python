#!/bin/env python3
__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."


import sys
import pprint
import argparse
import json

from mr_python.api.high_level import Auth as authenticate
from mr_python.api.high_level import Users as user


def parse_cli_args(
    program_name="get_users",
    desc="A mediumroast.io example utility that lists users using mr_python SDK.",
):
    parser = argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument(
        "--rest_url",
        help="The URL of the target REST server",
        type=str,
        dest="rest_url",
        default="http://mr-01:3000",
    )
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
        "--get_substudies",
        help="Get all substudies by status",
        type=str,
        dest="get_substudies",
        choices=["all", "unthemed"],
    )
    parser.add_argument(
        "--get_themes",
        help="Get all themes and their quotes for an individual study",
        type=str,
        dest="get_themes",
    )
    parser.add_argument(
        "--pretty_output",
        help="Specify if the STDOUT format is pretty printed or not",
        dest="pretty_output",
        action='store_true',
        default=False,
    )
    parser.add_argument(
        "--get_by_guid", help="Get study object by GUID", type=str, dest="by_guid"
    )
    parser.add_argument(
        "--get_by_name", help="Get study object by study name", type=str, dest="by_name"
    )
    parser.add_argument(
        "--user", help="User name", type=str, dest="user", default="foo"
    )
    parser.add_argument(
        "--secret", help="Secret or password", type=str, dest="secret", default="bar"
    )
    cli_args = parser.parse_args()
    return cli_args


if __name__ == "__main__":
    printer = pprint.PrettyPrinter(indent=1, compact=False)
    my_args = parse_cli_args()

    auth_ctl = authenticate(
        user_name=my_args.user, secret=my_args.secret, rest_server_url=my_args.rest_url
    )
    credential = auth_ctl.login()
    study_ctl = study(credential)
    resp = list()
    success = bool()
    if my_args.name_by_guid:
        success, resp = study_ctl.get_name_by_guid(my_args.name_by_guid)
    elif my_args.guid_by_name:
        success, resp = study_ctl.get_guid_by_name(my_args.guid_by_name)
    elif my_args.by_guid:
        success, resp = study_ctl.get_by_guid(my_args.by_guid)
    elif my_args.by_name:
        success, resp = study_ctl.get_by_name(my_args.by_name)
    elif my_args.get_substudies == "all":
        success, resp = study_ctl.get_substudies()
    elif my_args.get_substudies == "unthemed":
        success, resp = study_ctl.get_unthemed_substudies()
    elif my_args.get_themes:
        success, resp = study_ctl.get_themes(my_args.get_themes)
    else:
        success, resp = study_ctl.get_all()

    if success:
        if my_args.pretty_output:
            printer.pprint(resp)
        else:
            print(json.dumps(resp))

    else:
        print("CLI ERROR: This is a generic error message, as something went wrong.")
        sys.exit(-1)
