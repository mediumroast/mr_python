#!/bin/env python3

### Make a copy of this file for the official backend to load data from MINIO

__version__ = "1.0"
__author__ = "Michael Hay & Raul Flores"
__date__ = "2022-March-28"
__copyright__ = "Copyright 2022 mediumroast.io. All rights reserved."


import sys, argparse
from mr_python.transformers.company import Transform as xform_companies
from mr_python.transformers.study import Transform as xform_studies
from mr_python.transformers.interaction import Transform as xform_interactions
from mr_python.loaders.backend_functions import send_study, send_company, send_interaction
from json import loads

def extract_from_json(loc):
    raw_json = open(loc)
    # print(raw_json.read())
    return loads(raw_json.read())

def transform_studies(src_data, obj_type="Study", rewrite_dir="./"):
    # Create study objects
    print("Preparing to transform extracted data into [" + obj_type + "] objects.")
    xformer = xform_studies(rewrite_config_dir=rewrite_dir, debug=False)
    tgt = xformer.create_objects(src_data)
    return tgt


def transform_companies(src_data, obj_type="Company", rewrite_dir="./"):
    # Create company objects
    xformer = xform_companies(rewrite_config_dir=rewrite_dir, debug=False)
    tgt = xformer.create_objects(src_data)
    return tgt


def transform_interactions(src_data, obj_type="Interaction", rewrite_dir="./"):
    # Create interaction objects
    print("Preparing to transform extracted data into [" + obj_type + "] objects.")
    xformer = xform_interactions(rewrite_config_dir=rewrite_dir, debug=False)
    tgt = xformer.create_objects(src_data)
    sent = tgt["totalInteractions"]
    recieved = len(tgt["interactions"])
    if sent == recieved:
        return tgt

def parse_cli_args(
    program_name="json to database",
    desc="A mediumroast.io example utility that exercises ETLs to create a JSON file for usage in the Node.js json-server.",
):
    parser = argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument(
        "--file_location",
        help="File to be uploaded",
        type=str,
        dest="file_loc",
    )
    parser.add_argument(
        "--s3_access_key",
        help="S3 access key or user name",
        type=str,
        dest="s3_access_key",
    )
    parser.add_argument(
        "--s3_secret_key", help="S3 secret key", type=str, dest="s3_secret_key"
    )
    cli_args = parser.parse_args()
    return cli_args

def send_data(bucket, url):
    extracted_data = extract_from_json(my_args.file_loc)
    print
    ### Transform the extracted data into a proper JSON structure suitable for Node.js json-server

    ### Set up the basic object structure
    transformed_data = {
        "studies": [],
        "companies": [],
        "interactions": []
    }

    # Companies transformation
    # transformed_data["companies"] = transform_companies(
    #     extracted_data, rewrite_dir='./'
    # )["companies"]
    
    for comp in transformed_data["companies"]:
        send_company(comp)

    
    for study in transformed_data["studies"]:
        send_study(study)
    
    for interact in transformed_data["interactions"]:
        send_interaction(interact)


if __name__ == "__main__":
    # Establish a print function for better visibility, parse cli args, and setup
    my_args = parse_cli_args()

    # Extract the data from the source
    extracted_data = extract_from_json(my_args.file_loc)

    
    for comp in extracted_data["companies"]:
        send_company(comp)

    for study in extracted_data["studies"]:
        send_study(study)
    
    for interact in extracted_data["interactions"]:
        send_interaction(interact)
