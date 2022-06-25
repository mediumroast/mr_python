#!/usr/bin/python3

__version__ = "2.0"
__author__ = "Michael Hay"
__date__ = "2022-June-25"
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."


import sys
import pprint
import argparse
from mr_python.extractors.s3bucket import Extract as mr_extract_s3
from mr_python.transformers.company import Transform as xform_companies
from mr_python.transformers.study import Transform as xform_studies
from mr_python.transformers.interaction import Transform as xform_interactions



def extract_from_s3(s3_url, bucket_name="interactions"):
    # Capture the source data from the file specified in file_name
    print(
        "\nPreparing to extract data from source bucket [" + bucket_name + "]... Ok")
    src_obj = mr_extract_s3(bucket=bucket_name, url=s3_url)
    src_data = src_obj.get_data()
    no_items = len(src_data)
    print(
        "Extracted ["
        + str(no_items)
        + "] total items from source bucket ["
        + bucket_name
        + "]... OK"
    )
    return src_data


# TODO Transform the output into a string and hash it, we can then compare the hash across runs to verify correctness <-- Useful for testing

# TODO Create some README.md files to cover key thoughts around testing for the system
#   Starts with system setup of minio, running sample test scripts to ETL data, etc.


def transform_studies(src_data, obj_type="Study", rewrite_dir="./"):
    # Create study objects
    print(
        "Preparing to transform extracted data into [" + obj_type + "] objects.")
    xformer = xform_studies(rewrite_config_dir=rewrite_dir, debug=False)
    tgt = xformer.create_objects(src_data)
    recieved = len(tgt["studies"])
    print(
        "Transformed extracted data into study objects into ["
        + str(recieved)
        + "] ... Ok"
    )
    return tgt


def transform_companies(src_data, obj_type="Company", rewrite_dir="./"):
    # Create company objects
    print(
        "Preparing to transform extracted data into [" + obj_type + "] objects.")
    xformer = xform_companies(rewrite_config_dir=rewrite_dir, debug=False)
    tgt = xformer.create_objects(src_data)
    recieved = len(tgt["companies"])
    print(
        "Transformed extracted data into company objects into ["
        + str(recieved)
        + "] ... Ok"
    )
    return tgt


def transform_interactions(src_data, obj_type="Interaction", rewrite_dir="./"):
    # Create interaction objects
    print(
        "Preparing to transform extracted data into [" + obj_type + "] objects.")
    xformer = xform_interactions(rewrite_config_dir=rewrite_dir, debug=False)
    tgt = xformer.create_objects(src_data)
    sent = tgt["totalInteractions"]
    recieved = len(tgt["interactions"])
    print("Transformed extracted data into interaction objects ... Ok")
    if sent == recieved:
        print(
            "Successful transformation, sent ["
            + str(sent)
            + "] and recived ["
            + str(recieved)
            + "] transformations matched ... Ok"
        )
        return tgt
    else:
        print(
            "Failed transformation, sent ["
            + str(sent)
            + "] and recived ["
            + str(recieved)
            + "] transformations don't match, exiting... Failed"
        )
        sys.exit(-1)


def parse_cli_args(
    program_name="create_json_db",
    desc="A mediumroast.io example utility that exercises ETLs to create a JSON file for usage in the Node.js json-server.",
):
    parser = argparse.ArgumentParser(prog=program_name, description=desc)

    parser.add_argument(
        "--url",
        help="Using either IP or hostname the network address and port for the S3 compatible object store",
        type=str,
        dest="s3_url",
    )
    parser.add_argument(
        "--bucket",
        help="Define the bucket for the source data",
        type=str,
        dest="s3_bucket",
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


if __name__ == "__main__":
    # Establish a print function for better visibility, parse cli args, and setup
    printer = pprint.PrettyPrinter()
    my_args = parse_cli_args()


    # Extract the data from the source
    extracted_data = extract_from_s3(
        s3_url=my_args.s3_url, bucket_name=my_args.s3_bucket
    )

    # Set up the basic object structure
    transformed_data = {
        "studies": [],
        "companies": [],
        "interactions": [],
    }

    # Companies transformation
    transformed_data["companies"] = transform_companies(
        extracted_data, rewrite_dir=my_args.rewrite_config_dir
    )["companies"]

    # Studies transformation
    transformed_data["studies"] = transform_studies(
        extracted_data, rewrite_dir=my_args.rewrite_config_dir
    )["studies"]

    # Interactions transformation
    transformed_data["interactions"] = transform_interactions(
        extracted_data, rewrite_dir=my_args.rewrite_config_dir
    )["interactions"]

