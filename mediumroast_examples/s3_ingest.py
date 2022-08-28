#!/usr/bin/python3

__version__ = "2.0"
__author__ = "Michael Hay"
__date__ = "2022-June-25"
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Import system libraries
import pprint
import argparse
import pathlib
from xml.dom.pulldom import END_DOCUMENT
from xmlrpc.client import boolean
import pyfiglet

# Import utilities
from mediumroast_py.helpers import utilities as util

# Import authentication
from mediumroast_py.api.mr_server import Auth as authenticate

# Import extractor
from mediumroast_py.extractors.s3bucket import Extract as mr_extract_s3

# Import transformers
from mediumroast_py.transformers.company import Transform as xform_companies
from mediumroast_py.transformers.study import Transform as xform_studies
from mediumroast_py.transformers.interaction import Transform as xform_interactions

# Import backend modules for loading
from mediumroast_py.api.mr_server import Companies as company
from mediumroast_py.api.mr_server import Interactions as interaction
from mediumroast_py.api.mr_server import Studies as study


def extract_from_s3(s3_url, bucket_name="interactions"):
    # Capture the source data from the file specified in file_name
    print(
        "\nExtracting data from source bucket [" + bucket_name + "].")
    src_obj = mr_extract_s3(bucket=bucket_name, url=s3_url)
    src_data = src_obj.get_data()
    no_items = len(src_data)
    print(
        "\t-> Extracted ["
        + str(no_items)
        + "] total items from source bucket ["
        + bucket_name
        + "]."
    )
    print('-'*80, "\n")
    return src_data



# TODO Create some README.md files to cover key thoughts around testing for the system
#   Starts with system setup of minio, running sample test scripts to ETL data, etc.


def transform_studies(src_data, obj_type="Study", rewrite_rule_dir="./", debug=False):
    # Create study objects
    print(
        "Transforming raw data into [" + obj_type + "] objects.")
    xformer = xform_studies(rewrite_rule_dir, debug=debug)
    tgt = xformer.create_objects(src_data)
    recieved = len(tgt["studies"])
    print(
        "\t-> Transformed [" + str(recieved) + "] studies."
    )
    print('-'*80, "\n")
    return tgt


def transform_companies(src_data, obj_type="Company", rewrite_rule_dir="./", debug=False):
    # Create company objects
    print(
        "Transforming raw data into [" + obj_type + "] objects.")
    xformer = xform_companies(rewrite_rule_dir, debug=debug)
    tgt = xformer.create_objects(src_data)
    recieved = len(tgt["companies"])
    print(
        "\t-> Transformed [" + str(recieved) + "] companies."
    )
    print('-'*80, "\n")
    return tgt


def transform_interactions(src_data, obj_type="Interaction", rewrite_rule_dir="./", debug=False):
    # Create interaction objects
    print(
        "Transforming raw data into [" + obj_type + "] objects.")
    xformer = xform_interactions(rewrite_rule_dir, debug=debug)
    tgt = xformer.create_objects(src_data)
    recieved = len(tgt["interactions"])
    print(
        "\t-> Transformed [" + str(recieved) + "] interactions."
    )
    print('-'*80, "\n")
    return tgt



def parse_cli_args(
    program_name="s3_ingest",
    desc='Example CLI utility extracts source data from file names (stored in an S3 bucket), transforms them into' +
        ' Company, Study and Interaction objects, and then loads them into the mediumroast.io backend. Study, Company, ' +
        'and Interaction object metadata can be overwritten via the relevant files stored in "rewrite_rules/".',
):
    parser = argparse.ArgumentParser(prog=program_name, description=desc)

    # Gather system oriented configuration variables from the command line
    parser.add_argument(
        '--no_intro',
        help="Suppress the introductory text and get right to business.",
        dest='no_intro',
        action='store_false',
        default=False
    )
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
        "--s3_server",
        help="Using either IP or hostname the network address and port for the S3 compatible object store",
        type=str,
        dest="s3_server",
    )
    parser.add_argument(
        "--bucket",
        help="Define the bucket for the source data",
        type=str,
        dest="s3_bucket",
        required=True
    )
    parser.add_argument(
        "--access_key",
        help="S3 access key or user name",
        type=str,
        dest="s3_access_key",
    )
    parser.add_argument(
        "--secret_key", help="S3 secret key", type=str, dest="s3_secret_key"
    )

    parser.add_argument(
        "--rewrite_rule_dir",
        help="The full path to the directory containing files with rewrite rules",
        type=str,
        dest="rewrite_rule_dir",
        default="./rewrite_rules",
    )
    cli_args = parser.parse_args()
    return cli_args

def set_env(cli_args, config):
        """Set up the core environment variables and return a dict with them included.

        The order of priority for the arguments is:
            1. CLI switches are the first priority and override the config file
            2. The settings in the config file are used when no CLI switches are provided

        For users the preference should be to put key and common environmental variables into
        the configuration file to reduce the need for CLI switches.
        """
        # Explicitly set the essential environment variables to defaults or None
        env = {
            'rest_server': None,
            'user': None,
            'secret': None,
            'api_key': None,
            'server_type': None,
            's3_server': None,
            's3_bucket': cli_args.s3_bucket,
            's3_access_key': None,
            's3_secret_key': None,
            # S3 Region is presently unchanged for Minio, for AWS, etc. this would need to change
            's3_region': config['s3_settings']['region'],
            'rewrite_rule_dir': cli_args.rewrite_rule_dir
        }

        # Now set the environment up in the priority as documented above
        env['rest_server'] = cli_args.rest_server if cli_args.rest_server else config['DEFAULT']['rest_server']
        env['user'] = cli_args.user if cli_args.user else config['DEFAULT']['user']
        env['secret'] = cli_args.secret if cli_args.secret else config['DEFAULT']['secret']
        env['api_key'] = cli_args.api_key if cli_args.api_key else config['DEFAULT']['api_key']
        env['s3_server'] = cli_args.s3_server if cli_args.s3_server else config['s3_settings']['server']
        env['s3_access_key'] = cli_args.s3_access_key if cli_args.s3_access_key else config['s3_settings']['user']
        env['s3_secret_key'] = cli_args.s3_secret_key if cli_args.s3_secret_key else config['s3_settings']['api_key']

        return True, {"status_code": "SUCCEEDED"}, env


if __name__ == "__main__":

    # Create the utilities object
    my_utilities = util()

    # Establish a print function for better visibility, parse cli args, and setup
    printer = pprint.PrettyPrinter()
    my_args = parse_cli_args()
    [status, msg, my_config] = my_utilities.get_config_file(my_args.conf_file)
    [status, msg, my_env] = set_env(my_args, my_config)

    # Print intro unless suppressed
    if not my_args.no_intro:
        intro = pyfiglet.figlet_format('Mediumroast S3 Ingest utility.')
        print('-'*79, "\n", intro, "\n", '-'*79, "\n")

    # Perform authentication
    auth_ctl = authenticate(
        user=my_env['user'], 
        secret=my_env['secret'], 
        rest_server=my_env['rest_server'],
        api_key=my_env['api_key']
    )
    credential = auth_ctl.login()

    # Create the API controllers
    company_api_ctl = company(credential)
    interaction_api_ctl = interaction(credential)
    study_api_ctl = study(credential)

    # Extract the data from the source
    extracted_data = extract_from_s3(
        s3_url=my_env['s3_server'], bucket_name=my_env['s3_bucket']
    )

    # Set up the basic object structure
    transformed_data = {
        "studies": [],
        "companies": [],
        "interactions": [],
    }

    # Companies transformation
    transformed_data["companies"] = transform_companies(
        extracted_data, rewrite_rule_dir=my_env['rewrite_rule_dir']
    )["companies"]

    # Studies transformation
    transformed_data["studies"] = transform_studies(
        extracted_data, rewrite_rule_dir=my_env['rewrite_rule_dir']
    )["studies"]

    # Interactions transformation
    transformed_data["interactions"] = transform_interactions(
        extracted_data, rewrite_rule_dir=my_env['rewrite_rule_dir']
    )["interactions"]


    # Ingest the transformed objects one set at a time
    print('Ingesting all objects into the backend -- object ingest status: o = successful, x = failed.\n')
    for obj_type in ['interactions', 'companies', 'studies']:
        print("\t-> Ingesting transformed [" + obj_type + "] into the backend.")
        print('\t', end='')
        for obj_inst in transformed_data[obj_type]:
            if obj_type == 'companies':
                [success, msg, resp] = company_api_ctl.create_obj(obj_inst)
                if success: print('o', end='')
                else: print('x', end='')
            elif obj_type == 'interactions':
                [success, msg, resp] = interaction_api_ctl.create_obj(obj_inst)

                if success: print('o', end='')
                else: print('x', end='')
            elif obj_type == 'studies':
                [success, msg, resp] = study_api_ctl.create_obj(obj_inst)
                if success: print('o', end='')
                else: print('x', end='')
        print('\n')


