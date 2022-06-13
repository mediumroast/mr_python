# Introduction
This is the Python Software Development Kit (SDK) for the mediumroast.io.  Interal and proprietary tooling from Mediumroast, Inc. uses this SDK, so it will always be a first class citizen. Specifically, we build tools requiring ETL (Extract, Transform and Load), Machine Learning and Natural Language Processing (NLP) with this SDK. As appropriate examples illustrating various capabilities of the SDK can be found in the `examples/` directory of this package.  

# Installation and Configuration Steps for Developers
The following steps are important if you are developing or extending the Python SDK.  If you're not a developer these steps aren't as important to you and you should pay attention to section entitled *Installation for Early Adopters and Testers*.
## Cloning the repository for Developers
Assuming `git` is installed and your credentials are set up to talk to the mediumroast.io set of repositories it should be possible to do the following as a user on the system:
1. `mkdir ~/dev;cd ~/dev`
2. `git clone git@github.com:mediumroast/mr_sdk.git`
This will create an `mr_sdk` directory in `~/dev/` and allow you to proceed to the following steps for installation.

## Installation
For developers of the package the `setup.py` file is available to enable a local software distribution that can be improved upon.  As inspired by [this article](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html) the best current way to perform the installation of a developer version after cloning is to assuming you've cloned into `~/dev`:
1. `cd ~/dev/mr_sdk/python`
2. `sudo pip install -e ./`
With this accomplished tools that depend upon this package including the [mr_json_server](https://github.com/mediumroast/mr_json_server) and the [mr_caffeine](https://github.com/mediumroast/mr_caffeine) service should operate.  If there are issues encountered then please open an [issue](https://github.com/mediumroast/mr_sdk/issues).

## Structure of the repository
The following structure is available for the Python SDK, as new SDK implementations are created additional top level directories will be created.
```
mr_python/
      examples/
      mr_python/
            api/
            extractors/
            transformers/
            loaders/
            helpers.py
      setup.py
      README.md
      LICENSE
```
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
                 server_type = mr
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
server_type = mr
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
## get_users.py
```
usage: list_interactions [-h] [--rest_url REST_URL] [--get_name_by_guid NAME_BY_GUID] [--get_guid_by_name GUID_BY_NAME] [--get_url_by_guid URL_BY_GUID] [--get_abs_by_guid ABS_BY_GUID] [--get_by_guid BY_GUID]
                         [--get_by_name BY_NAME] [--get_all_unsummarized ALL_UNSUMMARIZED] [--user USER] [--secret SECRET]

A mediumroast.io example utility that lists interactions using mr_api.

optional arguments:
  -h, --help            show this help message and exit
  --rest_url REST_URL   The URL of the target REST server
  --get_name_by_guid NAME_BY_GUID
                        Get interaction name by GUID
  --get_guid_by_name GUID_BY_NAME
                        Get GUID by interaction name
  --get_url_by_guid URL_BY_GUID
                        Get interaction url by GUID
  --get_abs_by_guid ABS_BY_GUID
                        Get interaction abstract by GUID
  --get_by_guid BY_GUID
                        Get interaction object by GUID
  --get_by_name BY_NAME
                        Get interaction object by interaction name
  --get_all_unsummarized ALL_UNSUMMARIZED
                        Get all interactions that are unsummarized
  --user USER           User name
  --secret SECRET       Secret or password
```
### Example output
```
./list_interactions.py --get_by_guid=a1049f53de0929252fd6b655be1da37ae9ed27fe44f2814b5f0f9e102b7cabd3
{'GUID': 'a1049f53de0929252fd6b655be1da37ae9ed27fe44f2814b5f0f9e102b7cabd3',
 'abstract': 'Question asked by Andrew J.  2 replies 5 months ago Advice to '
             'deﬁne our PM process? -Andrew   2 Replies Bryan McCarty Product '
             'Management and  5 months ago In my last product role, I was in '
             'this same spot. Myself and one other PM were brought in to a '
             'startup that was recently acquired. The ﬁrst thing we did was '
             'get our products and the various backlog '
             'spreadsheets/ideas/features into  And yes, I now work at  but '
             'this was long before I joined the team. It also made us agree on '
             'goals for the quarter and connect all of our work to those '
             "agreed-upon goals. Another resource that may help is Intercom's "
             'podcast. It always gave me good process-related ideas that I '
             'could implement. They interview product leaders from all sorts '
             "of companies so there's a variety of perspectives.. I bet some "
             'of the episodes in the archives would directly answer the '
             "questions you've listed.",
 'contactAddress': 'Unknown',
 'contactEmail': 'Unknown',
 'contactLinkedIn': 'Unknown',
 'contactName': 'Unknown',
 'contactPhone': 'Unknown',
 'contactTwitter': 'Unknown',
 'contactZipPostal': 'Unknown',
 'date': '20191221',
 'id': 'a1049f53de0929252fd6b655be1da37ae9ed27fe44f2814b5f0f9e102b7cabd3',
 'interactionName': '201912212100-Customer Insights-Aha',
 'interactionType': 'Interview',
 'latitude': 32.71568000000008,
 'linkedCompanies': {'Aha': '6dbfa33b06706033931b0154210fbcb5fafb995315eccfbd8bc5b12d5e5569f7'},
 'linkedStudies': {'Customer Insights': 'f3eae874b1fba924e81d5963a2bc7752ab8d2acd906bb2944f6243f163a6bf23'},
 'longitude': -117.16170999999997,
 'notes': {'1': {'2099': "This is an example note created for the 'Interaction "
                         "Object: [201912212100-Customer Insights-Aha]' object "
                         'on Mon Sep 27 00:42:05 2021 by a Mediumroast SDK '
                         'load utility.'}},
 'public': False,
 'simpleDesc': 'Learn from Aha, either in person or digitally, key points and '
               'inputs related to the study Customer Insights',
 'state': 'summarized',
 'status': 'Canceled',
 'thumbnail': 's3://mr-02:9000/interactions/thumb_201912212100-AMER-US-CA-SAN '
              'DIEGO-ICT-Customer Insights-Aha-Online.pdf.png',
 'time': '2100',
 'totalCompanies': 1,
 'totalStudies': 1,
 'url': 's3://mr-02:9000/interactions/201912212100-AMER-US-CA-SAN '
        'DIEGO-ICT-Customer Insights-Aha-Online.pdf'}
```