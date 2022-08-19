# The examples
The following examples have been built to illustrate how to interact with the mediumroast.io application.

## Step 1: env_setup.py
The start of your journey begins with the creation of a proper environment with relevant server name, server type, user name, password, API key, etc. definitions.  This python program will guide you through the process of creating a 
`~/.mediumroast/config.ini` file which records the key information needed to talk to the mediumroast.io backend.
Note, this script will not create critical information like your API key, user name and so on.  Therefore you will
need this information on hand to properly setup your environment for the examples to run or to use the Python
SDK for development.

### Example output
```
./env_setup.py 
 __  __          _ _                                     _   
|  \/  | ___  __| (_)_   _ _ __ ___  _ __ ___   __ _ ___| |_ 
| |\/| |/ _ \/ _` | | | | | '_ ` _ \| '__/ _ \ / _` / __| __|
| |  | |  __/ (_| | | |_| | | | | | | | | (_) | (_| \__ \ |_ 
|_|  |_|\___|\__,_|_|\__,_|_| |_| |_|_|  \___/ \__,_|___/\__|
                                                             
  ____ _     ___    ___    ____ ___            _                
 / ___| |   |_ _|  / / \  |  _ \_ _|  ___  ___| |_ _   _ _ __   
| |   | |    | |  / / _ \ | |_) | |  / __|/ _ \ __| | | | '_ \  
| |___| |___ | | / / ___ \|  __/| |  \__ \  __/ |_| |_| | |_) | 
 \____|_____|___/_/_/   \_\_|  |___| |___/\___|\__|\__,_| .__(_)
                                                        |_|     
 
 -------------------------------------------------------------------------------- 

Checking to see if the the target configuration file [/home/mihay42/.mediumroast/config.ini] already exists.
Target configuration file not detected, proceeding...

Setting up the environment for mediumroast.io...
IP address or host name of mediumroast.io server, default [http://mr-02:6767]: 
Your mediumroast.io user name, default [rflores]: 
The password for your user name: 
The API key for the mediumroast.io server: 
Define the server type for the mediumroast.io backend, default [mr]: 
Specify the working directory for the CLI, default [/tmp]: 

Verifying the current environmental settings...
                 rest_server = http://mr-02:6767
                 user = rflores
                 secret = [suppressed]
                 api_key = [suppressed]
                 working_dir = /tmp
Are these environmental settings correct? [Y/n] 

Saving the current environmental settings...
```

### Example ~/.mediumroast/config.ini
While the details of the configuration file aren't documented here an example output run from the `env_setup.py` program
is provided to reference.
```
[DEFAULT]
rest_server = http://mr-02:6767
user = rflores
secret = [Suppressed]
api_key = [Suppressed]
working_dir = /tmp

[s3_credentials]
user = medium_roast_io
api_key = [Suppressed]
server = http://mr-03:9000
source = openvault
region = in-the-closet

[document_settings]
font_type = Avenir Next
font_size = 10
title_font_color = #41a6ce
title_font_size = 22
company = Mediumroast, Inc.
copyright = Copyright 2022, Mediumroast. All rights reserved.
output_dir = Documents
```
## Step 2. Running the example CLI utlities
There are example Command Line Interfaces (CLI) for each of the four object types: users, companies, interactions and studies.  Accompanying each CLI is a JSON document that includes some sample data to ingest into the backend.  While in a programmatic implementation the intermediate step of creating a JSON document is largely not required having examples is a handy way to understand the minimum set of attributes each object type requires.  Additionally, all CLIs are an implementation of the `base_cli.py` module.  This ensures that as much as possible the structure of the command line switches is consistent across all implementations.  Further the `base_cli.py` acts as a kind of reference implemetation showing how to get, create, update and delete objects.  Feel free to borrow and reference the `run_cli` method in `MrCLI` class found within `base_cli.py` when considering how to work with the mediumroast.io application.

Since all CLI implementations are largely tne same what follows is an example of `company.py` starting from usage information, example runs and outputs. Note that since the tools are still in development some of the outputs you see when using these utilities might differ from what is in this README.

### company.py - usage
```
$USER>~/dev/mr_python/examples$ ./company.py --help
usage: company [-h] [--conf_file CONF_FILE] [--rest_url REST_SERVER] [--api_key API_KEY] [--user USER]
               [--secret SECRET] [--pretty_output] [--get_name_by_id NAME_BY_ID] [--get_id_by_name ID_BY_NAME] [--get_by_id BY_ID]
               [--get_by_x BY_X] [--get_by_name BY_NAME] [--create JSON_OBJ] [--update UPDATE_OBJ] [--delete OBJ_ID]

Example CLI utility to get and manipulate company information in the mediumroast.io backend.

optional arguments:
  -h, --help            show this help message and exit
  --conf_file CONF_FILE
                        Fully qualified filename for storing the configuration variables.
  --rest_url REST_SERVER
                        The URL of the target REST server
  --api_key API_KEY     The API key needed to talk to the backend
  --server_type {json,mr}
                        The API key needed to talk to the backend
  --user USER           User name
  --secret SECRET       Secret or password
  --pretty_output       Specify if the STDOUT format is pretty printed or not
  --get_name_by_id NAME_BY_ID
                        Get study name by GUID
  --get_id_by_name ID_BY_NAME
                        Get GUID by study name
  --get_by_id BY_ID     Get object by ID
  --get_by_x BY_X       Get object by an arbitrary attribute as specified by JSON (ex '{"zip_postal":"92131"}')
  --get_by_name BY_NAME
                        Get object by name
  --create JSON_OBJ     Add an object to the backend by specifying a JSON file
  --update UPDATE_OBJ   Update an object from the backend by specifying the object's id and value to update in JSON
  --delete OBJ_ID       Delete an object from the backend by specifyin the object's id
$USER>~/dev/mr_python/examples$ ./interaction.py --create=./interactions_example.py
```

### company.py - create companies
```
$USER>~/dev/mr_python/examples$ ./company.py --create=./companies_example.json
Successfully created [4] company objects, exiting.
```

### company.py - get all companies
```
$USER>~/dev/mr_python/examples$ ./company.py
[{'cik': 'None',
  'city': 'San Diego',
  'country': 'US',
  'description': 'A San Diego base Software as a Service company focused on '
                 'empowering Products, Sellers and Customer Success Managers '
                 'with customer, competitive, partner and more generally '
                 'market insights.',
  'icon': 'Unknown',
  'id': 1,
  'industry': '7372—Prepackaged Software',
  'latitude': 32.89969,
  'logo_url': 'Unknown',
  'longitude': -117.09562,
  'name': 'Mediumroast, Inc.',
  'phone': 'None',
  'recent10k_url': 'None',
  'recent10q_url': 'None',
  'region': 'AMER',
  'role': 'Partner',
  'state_province': 'CA',
  'stock_symbol': 'None',
  'street_address': '10181 Scripps Gateway Ct',
  'url': 'https://mediumroast.io',
  'zip_postal': '92131'},
 {'cik': '816761',
  'city': 'San Diego',
  'country': 'US',
  'description': 'Teradata Corporation is an American software company that '
                 'provides database and analytics-related software, products, '
                 'and services. The company was formed in 1979 in Brentwood, '
                 'California, as a collaboration between researchers at '
                 "Caltech and Citibank's advanced technology group.",
  'icon': 'Unknown',
  'id': 2,
  'industry': '7371—Computer Programming Services',
  'latitude': 33.02233,
  'logo_url': 'Unknown',
  'longitude': -117.09237,
  'name': 'Teradata, Inc.',
  'phone': '1-866-548-8348',
  'recent10k_url': 'https://www.sec.gov/ix?doc=/Archives/edgar/data/816761/000081676122000009/tdc-20211231.htm',
  'recent10q_url': 'https://www.sec.gov/ix?doc=/Archives/edgar/data/816761/000081676122000015/tdc-20220331.htm',
  'region': 'AMER',
  'role': 'Partner',
  'state_province': 'CA',
  'stock_symbol': 'TDC',
  'street_address': '17095 VIA DEL CAMPO',
  'url': 'https://www.teradata.com',
  'zip_postal': '92127'},
 {'cik': 'Not Applicable',
  'city': 'Tokyo',
  'country': 'JAPAN',
  'description': 'Hitachi, Ltd. is a Japanese multinational conglomerate '
                 'corporation headquartered in Chiyoda, Tokyo, Japan. It is '
                 'the parent company of the Hitachi Group and had formed part '
                 'of the Nissan zaibatsu and later DKB Group and Fuyo Group of '
                 'companies before DKB and Fuji Bank merged into the Mizuho '
                 'Financial Group.',
  'icon': 'Unknown',
  'id': 3,
  'industry': 'Industrial Goods & Services Companies',
  'latitude': 35.670993,
  'logo_url': 'Unknown',
  'longitude': 139.749375,
  'name': 'Hitachi, Ltd.',
  'phone': '+81-3-3258-1111',
  'recent10k_url': 'https://www.hitachi.com/IR-e/library/stock/hit_sr_fy2020_4_en.pdf',
  'recent10q_url': 'https://www.hitachi.com/IR-e/library/stock/hit_sr_fy2021_3_en.pdf',
  'region': 'APAC',
  'role': 'Partner',
  'state_province': 'Tokyo',
  'stock_symbol': 'Hitachi (TSE)',
  'street_address': '6-6, Marunouchi 1-chome, Chiyoda-ku',
  'url': 'https://www.hitachi.com/',
  'zip_postal': '100-8280'},
 {'cik': 'Not Applicable',
  'city': 'Armonk',
  'country': 'USA',
  'description': 'Corporation is an American multinational technology '
                 'corporation headquartered in Armonk, New York, with '
                 'operations in over 171 countries. The company began in 1911, '
                 'founded in Endicott, New York, by trust businessman Charles '
                 'Ranlett Flint, as the Computing-Tabulating-Recording Company '
                 "and was renamed 'International Business Machines' in 1924.",
  'icon': 'Unknown',
  'id': 4,
  'industry': 'Software, Internet & Computer Services',
  'latitude': 41.10823,
  'logo_url': 'Unknown',
  'longitude': -73.72032,
  'name': 'International Business Machine, Corp.',
  'phone': '+1-914-499-1900',
  'recent10k_url': 'https://www.sec.gov/ix?doc=/Archives/edgar/data/51143/000155837022001584/ibm-20211231x10k.htm',
  'recent10q_url': 'https://www.sec.gov/ix?doc=/Archives/edgar/data/51143/000155837022005983/ibm-20220331x10q.htm',
  'region': 'AMER',
  'role': 'Partner',
  'state_province': 'New York',
  'stock_symbol': 'IBM',
  'street_address': '1 NEW ORCHARD RD',
  'url': 'https://www.ibm.com/',
  'zip_postal': '10504'}]
```

## Step 3: Ingestion utilities
Within the examples are ingestion utilties enabling bulk ingestion into the mediumroast.io from retained assets.  One of the utiltiies, `s3_ingest.py`, assumes that the file name includes key metadata for company, study and interaction objects.  Other utilities, as they are developed, will make less assumption about the file name structure.  

### s3_ingest.py
As in the name this utility takes metadata from an S3 bucket, transforms it into relevant objects and ingests the results in the 
mediumroast.io application.  It keys off an object naming structure to do its magic (defined below), and is combined with the mediumroast.io SDK ETL (Extract, Transform and Load) logic for rich object definition.  A key aspect of the transformation logic
includes what we've called rewrite rules.  These rules can act as a kind of override to discovered metadata.  The ingest utility 
will look for rewrite rules in the `examples/rewrite_rules` directory from this distribution, but this you can set the location
to your liking with the command line option `--rewrite_rule_dir REWRITE_RULE_DIR`.  Documentation for using the rewrite rules can be
found in [examples/rewrite_rules/README.md](https://github.com/mediumroast/mediumroast_py/tree/main/examples/rewrite_rules)

#### Object naming structure
This utility assumes the following structure for objects stored within an S3 bucket individual fields are separated by a dash or `-`.  One key assumption is that an object corresponds to a mediumroast.io interaction object, and the metadata is meant to enable the
creation of associated study and company objects.
1. Date - Definition: The date of the interaction; Format: YYYYMMDDHHMM; Example: 201402241004
2. Region - Definition: The region where the interaction took place; Format: one of AMER, EMEA, APAC; Example: APAC
3. Country - Definition: The country where the interaction took place; Format: N/A; Example: US
4. State/Province - Definition: The state/province where the interaction took place; Format: N/A; Example: California
5. City - Definition: The city where the interaction took place; Format: N/A; Example: Santa Clara
6. Industry - Definition: The industry for the company the interaction is associated to; Format: N/A; Example: Finance
7. Study - Definition: The study the interaction is associated to; Format: N/A; Example: Customer Insights
8. Company - Definition: The company the interaction is associated to; Format: N/A; Example: HDS
9. Interaction Type - Definition: The type of interaction performed; Format: N/A; Example: interview
An example fully assembled file name is represented below.
```
201402241004-AMER-US-CA-SANTA CLARA-ICT-Caffeine Customer Insights-HDS-Interview.pdf
```

#### Usage information for s3_ingest.py
```
usage: s3_ingest [-h] [--no_intro] [--conf_file CONF_FILE] [--mr_backend_url REST_SERVER] [--api_key API_KEY] [--server_type {json,mr}] [--user USER] [--secret SECRET]
                 [--s3_server S3_SERVER] --bucket S3_BUCKET [--access_key S3_ACCESS_KEY] [--secret_key S3_SECRET_KEY] [--rewrite_rule_dir REWRITE_RULE_DIR]

Example CLI utility extracts source data from file names (stored in an S3 bucket), transforms them into Company, Study and Interaction objects, and then loads them into the mediumroast.io backend. Study, Company, and Interaction object metadata can be overwritten via the relevant files stored in "rewrite_rules/".

optional arguments:
  -h, --help            show this help message and exit
  --no_intro            Suppress the introductory text and get right to business.
  --conf_file CONF_FILE
                        Fully qualified filename for storing the configuration variables.
  --mr_backend_url REST_SERVER
                        The URL of the target mediumroast.io server
  --api_key API_KEY     The API key needed to talk to the mediumroast.io server
  --server_type {json,mr}
                        The API key needed to talk to the backend
  --user USER           User name
  --secret SECRET       Secret or password
  --s3_server S3_SERVER
                        Using either IP or hostname the network address and port for the S3 compatible object store
  --bucket S3_BUCKET    Define the bucket for the source data
  --access_key S3_ACCESS_KEY
                        S3 access key or user name
  --secret_key S3_SECRET_KEY
                        S3 secret key
  --rewrite_rule_dir REWRITE_RULE_DIR
                        The full path to the directory containing files with rewrite rules
```
#### Example video


https://user-images.githubusercontent.com/10818650/178090055-d0d01ab0-8710-4033-8f31-f2863ec5bc75.mp4

