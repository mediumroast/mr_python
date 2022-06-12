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
mr_sdk/
        python/
            cli/
            dist/
            mediumroast/
                  api/
                  extractors/
                  transformers/
                  loaders/
                  helpers.py
            setup.py
            README.md
            LICENSE
```
# The CLI, Command Line Interface
The following example CLI wrappers have been built that wrap the sample API implementation and other elements in the SDK.  As appropriate example outputs are also included in the documentation.
## list_companies.py
```
usage: list_companies [-h] [--rest_url REST_URL] [--get_name_by_guid NAME_BY_GUID] [--get_guid_by_name GUID_BY_NAME] [--get_iterations {all,unthemed,unsummarized}] [--get_by_guid BY_GUID] [--get_by_name BY_NAME]
                      [--user USER] [--secret SECRET]

A mediumroast.io example utility that lists companies using mr_api.

optional arguments:
  -h, --help            show this help message and exit
  --rest_url REST_URL   The URL of the target REST server
  --get_name_by_guid NAME_BY_GUID
                        Get company name by GUID
  --get_guid_by_name GUID_BY_NAME
                        Get GUID by company name
  --get_iterations {all,unthemed,unsummarized}
                        Get all iterations or by status
  --get_by_guid BY_GUID
                        Get company object by GUID
  --get_by_name BY_NAME
                        Get company object by company name
  --user USER           User name
  --secret SECRET       Secret or password
```
### Example output
```
./list_companies.py --get_by_guid=6dbfa33b06706033931b0154210fbcb5fafb995315eccfbd8bc5b12d5e5569f7
{'GUID': '6dbfa33b06706033931b0154210fbcb5fafb995315eccfbd8bc5b12d5e5569f7',
 'Recent10kURL': 'Unknown',
 'Recent10qURL': 'Unknown',
 'cik': 'Unknown',
 'city': 'SAN DIEGO',
 'companyName': 'Aha',
 'country': 'US',
 'id': '6dbfa33b06706033931b0154210fbcb5fafb995315eccfbd8bc5b12d5e5569f7',
 'industry': 'Services | Business Services | Computer Programming, Data '
             'Processing, And Other Computer Related Services',
 'iterations': {'default': {'interactions': {'201912151800-Customer Insights-Aha': {'guid': 'd42ba72ab7317dea495dbef9fd7a4b18e220316689059d5ce87134a68033ed6a',
                                                                                    'state': 'unsummarized'},
                                             '201912151900-Customer Insights-Aha': {'guid': '2975c26e6ac058eaa6617949e4be59c14ed8da69d49168f2b7e11eedc7ff689c',
                                                                                    'state': 'unsummarized'},
                                             '201912152000-Customer Insights-Aha': {'guid': '03d225af95bc8d9ae1af795cae25b1f98afd886d3772e7b56b1899642fdbf8fc',
                                                                                    'state': 'unsummarized'},
                                             '201912161800-Customer Insights-Aha': {'guid': '203719812f4d2b7d986f134c81c7e01ff0b7ec0a454351ac020b3fc23ee7209f',
                                                                                    'state': 'unsummarized'},
                                             '201912161900-Customer Insights-Aha': {'guid': '9c9703bd9ea5aa58fbec75da5b7a67848a2c69efb34d6b82bdd43f4dca700c1a',
                                                                                    'state': 'unsummarized'},
                                             '201912162000-Customer Insights-Aha': {'guid': '440a968c8ec519d046a2064e4c1704307499f013eca6fae639cebdc6a1d31080',
                                                                                    'state': 'unsummarized'},
                                             '201912171800-Customer Insights-Aha': {'guid': 'cf22d4ac4c07fa502fdf507237396cc919b99ca6d5e20ede53fc0c65c3657886',
                                                                                    'state': 'unsummarized'},
                                             '201912171900-Customer Insights-Aha': {'guid': 'adcdc8c0c4e27ef6617cf61927253473986103662e9b1a0c7e3d0b4c93de41f2',
                                                                                    'state': 'unsummarized'},
                                             '201912172000-Customer Insights-Aha': {'guid': '02e5fbd561ae1ab679b793644c5bcf50fb26163623e35c2ff1a76f44f1022a46',
                                                                                    'state': 'unsummarized'},
                                             '201912181800-Customer Insights-Aha': {'guid': '29581d790d073ab20b1d7814f6c777944b601d038a59a5a9553f47eb29aa20c7',
                                                                                    'state': 'unsummarized'},
                                             '201912181900-Customer Insights-Aha': {'guid': '2599cac8d57cc536b8f46b55f4b90a265af000faf09785aebf37303179dbc61b',
                                                                                    'state': 'unsummarized'},
                                             '201912182000-Customer Insights-Aha': {'guid': '70cd002264a60361fcea43bfeb5bca9b6cfc05364b377530581a7317cbad69e4',
                                                                                    'state': 'unsummarized'},
                                             '201912191800-Customer Insights-Aha': {'guid': 'a0ec3c225c1b5a6df8444955c56d458b6920a91df7417a4a8b19babfd223401d',
                                                                                    'state': 'unsummarized'},
                                             '201912191900-Customer Insights-Aha': {'guid': '167c7dc72ed236c70c165e510de251d635d20116922068e8dc4579d6277e2725',
                                                                                    'state': 'unsummarized'},
                                             '201912192000-Customer Insights-Aha': {'guid': 'c812a6f111acfb353ba944f3c536334a1c15fb2663c3dd62ca6e0f78208eaf7f',
                                                                                    'state': 'unsummarized'},
                                             '201912201800-Customer Insights-Aha': {'guid': '02e4f0587d9426d4d9aa26d88eff656b35058c250ee58703ecb88e187bc6ca31',
                                                                                    'state': 'unsummarized'},
                                             '201912201900-Customer Insights-Aha': {'guid': '7f0b7da04a4919c7bc4a2e676fb916e0cc1465deaeadc9d74008baf28268c74c',
                                                                                    'state': 'unsummarized'},
                                             '201912202000-Customer Insights-Aha': {'guid': 'fe57ff2b168359e14950b6f46c45a891494b90651adf784096ecd7d4fdd0f003',
                                                                                    'state': 'unsummarized'},
                                             '201912211800-Customer Insights-Aha': {'guid': 'cdb15ae893120080c7cef65f23c0a7f0ed16942077a6b3af7be1f2c6fc8fe63a',
                                                                                    'state': 'unsummarized'},
                                             '201912211900-Customer Insights-Aha': {'guid': '60438bac13b7fab03a9d48062b1764ffb627acec94403c0eec79185d6771b448',
                                                                                    'state': 'unsummarized'},
                                             '201912212000-Customer Insights-Aha': {'guid': '1255026e832da09862cf55623ea0a78d795aa10a12522860e7720c6e3664de16',
                                                                                    'state': 'unsummarized'},
                                             '201912212100-Customer Insights-Aha': {'guid': 'a1049f53de0929252fd6b655be1da37ae9ed27fe44f2814b5f0f9e102b7cabd3',
                                                                                    'state': 'unsummarized'}},
                            'state': 'unthemed_unsummarized',
                            'totalInteractions': 22},
                'state': 'unthemed_unsummarized',
                'totalInteractions': 22,
                'totalIterations': 1},
 'latitude': 32.71568000000008,
 'linkedInteractions': {'201912151800-Customer Insights-Aha': 'd42ba72ab7317dea495dbef9fd7a4b18e220316689059d5ce87134a68033ed6a',
                        '201912151900-Customer Insights-Aha': '2975c26e6ac058eaa6617949e4be59c14ed8da69d49168f2b7e11eedc7ff689c',
                        '201912152000-Customer Insights-Aha': '03d225af95bc8d9ae1af795cae25b1f98afd886d3772e7b56b1899642fdbf8fc',
                        '201912161800-Customer Insights-Aha': '203719812f4d2b7d986f134c81c7e01ff0b7ec0a454351ac020b3fc23ee7209f',
                        '201912161900-Customer Insights-Aha': '9c9703bd9ea5aa58fbec75da5b7a67848a2c69efb34d6b82bdd43f4dca700c1a',
                        '201912162000-Customer Insights-Aha': '440a968c8ec519d046a2064e4c1704307499f013eca6fae639cebdc6a1d31080',
                        '201912171800-Customer Insights-Aha': 'cf22d4ac4c07fa502fdf507237396cc919b99ca6d5e20ede53fc0c65c3657886',
                        '201912171900-Customer Insights-Aha': 'adcdc8c0c4e27ef6617cf61927253473986103662e9b1a0c7e3d0b4c93de41f2',
                        '201912172000-Customer Insights-Aha': '02e5fbd561ae1ab679b793644c5bcf50fb26163623e35c2ff1a76f44f1022a46',
                        '201912181800-Customer Insights-Aha': '29581d790d073ab20b1d7814f6c777944b601d038a59a5a9553f47eb29aa20c7',
                        '201912181900-Customer Insights-Aha': '2599cac8d57cc536b8f46b55f4b90a265af000faf09785aebf37303179dbc61b',
                        '201912182000-Customer Insights-Aha': '70cd002264a60361fcea43bfeb5bca9b6cfc05364b377530581a7317cbad69e4',
                        '201912191800-Customer Insights-Aha': 'a0ec3c225c1b5a6df8444955c56d458b6920a91df7417a4a8b19babfd223401d',
                        '201912191900-Customer Insights-Aha': '167c7dc72ed236c70c165e510de251d635d20116922068e8dc4579d6277e2725',
                        '201912192000-Customer Insights-Aha': 'c812a6f111acfb353ba944f3c536334a1c15fb2663c3dd62ca6e0f78208eaf7f',
                        '201912201800-Customer Insights-Aha': '02e4f0587d9426d4d9aa26d88eff656b35058c250ee58703ecb88e187bc6ca31',
                        '201912201900-Customer Insights-Aha': '7f0b7da04a4919c7bc4a2e676fb916e0cc1465deaeadc9d74008baf28268c74c',
                        '201912202000-Customer Insights-Aha': 'fe57ff2b168359e14950b6f46c45a891494b90651adf784096ecd7d4fdd0f003',
                        '201912211800-Customer Insights-Aha': 'cdb15ae893120080c7cef65f23c0a7f0ed16942077a6b3af7be1f2c6fc8fe63a',
                        '201912211900-Customer Insights-Aha': '60438bac13b7fab03a9d48062b1764ffb627acec94403c0eec79185d6771b448',
                        '201912212000-Customer Insights-Aha': '1255026e832da09862cf55623ea0a78d795aa10a12522860e7720c6e3664de16',
                        '201912212100-Customer Insights-Aha': 'a1049f53de0929252fd6b655be1da37ae9ed27fe44f2814b5f0f9e102b7cabd3'},
 'linkedStudies': {'Customer Insights': 'f3eae874b1fba924e81d5963a2bc7752ab8d2acd906bb2944f6243f163a6bf23'},
 'longitude': -117.16170999999997,
 'notes': {'1': {'2098': "This is an example note created for the 'Company "
                         "Object: [Aha]' object on Mon Sep 27 00:41:36 2021 by "
                         'a Mediumroast SDK load utility.'}},
 'phone': 'Unknown',
 'region': 'AMER',
 'role': 'Competitor',
 'simpleDesc': 'A maker of roadmapping and product management technologies',
 'stateProvince': 'CA',
 'stockSymbol': 'Unknown',
 'streetAddress': 'Unknown',
 'totalInteractions': 22,
 'totalStudies': 1,
 'url': 'Unknown',
 'zipPostal': 'Unknown'}
```
## list_interactions.py
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

## list_raw_objects.py
A basic utility that talks to the `mr_minio` service and lists the raw objects for eventual transformation and loading.
## list_studies.py
```
usage: list_studies [-h] [--rest_url REST_URL] [--get_name_by_guid NAME_BY_GUID] [--get_guid_by_name GUID_BY_NAME] [--get_iterations {all,unthemed,unsummarized}] [--get_questions GET_QUESTIONS] [--get_by_guid BY_GUID]
                    [--get_by_name BY_NAME] [--user USER] [--secret SECRET]

A mediumroast.io example utility that lists studies using mr_api.

optional arguments:
  -h, --help            show this help message and exit
  --rest_url REST_URL   The URL of the target REST server
  --get_name_by_guid NAME_BY_GUID
                        Get study name by GUID
  --get_guid_by_name GUID_BY_NAME
                        Get GUID by study name
  --get_iterations {all,unthemed,unsummarized}
                        Get all iterations or by status
  --get_questions GET_QUESTIONS
                        Get all questions
  --get_by_guid BY_GUID
                        Get study object by GUID
  --get_by_name BY_NAME
                        Get study object by study name
  --user USER           User name
  --secret SECRET       Secret or password
```
### Example output
```
./list_studies.py --get_by_guid=f3eae874b1fba924e81d5963a2bc7752ab8d2acd906bb2944f6243f163a6bf23
{'GUID': 'f3eae874b1fba924e81d5963a2bc7752ab8d2acd906bb2944f6243f163a6bf23',
 'description': 'Work to realize a SaaS intently focused on revealing and '
                'solving problems for Customer and\n'
                'Competitive interactions which can make Customer Success and '
                'Product Management disciplines stronger.',
 'document': {'Action': {'1': 'Synthesize the 2014 and 2019 interactions into '
                              'a single study, analyze and uncover any '
                              'weaknesses. | Status: Done',
                         '2': 'Perform interviews, document these as '
                              'interactions and ingest into the mediumroast.io '
                              'to help remedy the weaknesses of previous '
                              'interactions. | Status: In process',
                         '3': 'Model and manage this Customer Insights study '
                              'in the mediumroast.io | Status: In process',
                         '4': 'Revamp the user experiences and associated '
                              'backend to follow the new findings. | Status: '
                              'In process',
                         'text': 'To improve completeness of this study the '
                                 'following actions and next steps are '
                                 'documented with appropriate statuses.'},
              'Introduction': 'This Customer Insights study includes two '
                              'phases separated by 5 years.  The first phase '
                              'was performed as as a part of a 2014 research '
                              'project that emphasized A/B testing for a '
                              'customer study indexing application.\n'
                              'While the second phase, conducted in late 2019, '
                              'both uncovered new themes and validated key '
                              'ideas surfaced in the first phase.  In the '
                              'second phase the emphasis was to investigate a '
                              'single competitor/partner candidate, Aha!, to\n'
                              'to determine if the key themes, detected within '
                              'the first phase, had or had not been already '
                              'addressed.  While details are accounted for in '
                              'the Opportunities section, the conclusion is '
                              'that the themes still largely remain unsolved\n'
                              'by companies who build tools for product '
                              'management, project management, and program '
                              'management disciplines.  Further, research '
                              'continues to test both the user experience and '
                              'refine elements of these\n'
                              'key themes with product managers at companies '
                              'like Ring Central, Google, Chaos Search, and so '
                              'on.',
              'Opportunity': {'1': 'Formalize Product Relationship Management '
                                   '- Tooling and associated process is needed '
                                   'to enable the build out of the community '
                                   'around the product management team.',
                              '2': 'Outlive the Product Manager across the '
                                   'entire lifecycle - Product managers are '
                                   'not always present throughout an entire '
                                   'program lifecycle or may leave the company '
                                   'making it essential that source materials '
                                   'and decisioning reasoning stands alone.',
                              '3': 'Integrate critical stakeholders via '
                                   'tooling - Product Managers are a key part '
                                   'of an overall program, but they do no live '
                                   'on an island making tooling access for a '
                                   'diverse set of stakeholders required.',
                              '4': 'Reduce the time and effort of product '
                                   'research and feedback correlation - '
                                   'Discerning the core whys and whats of any '
                                   'offer is super critical, but the path to '
                                   'get there is often slow and '
                                   'intransparent.  Therefore, tooling should\n'
                                   'drive speed, improve transparency and '
                                   'reduce work burden.',
                              '5': 'Forward and backward Traceability from '
                                   'problem to solution - While modern product '
                                   'management and roadmapping tooling '
                                   'facilitates process transparency, getting '
                                   'to clear and key whys and whats is '
                                   'frequently opaque and\n'
                                   'untraceable.  Clearly, revealing the path '
                                   'from problem identication, the whys, to '
                                   'problem resolution, the whats, is a key '
                                   'opportunity for tooling.',
                              '6': 'Intelligent Information Integration by '
                                   'connecting Productivity, CRM, Support, PM '
                                   'tools - New tooling cannot exist in an '
                                   'island therefore any opportunity requires '
                                   'integration into a user/customer '
                                   'ecosystem.',
                              '7': 'Visibility and Reporting for relevant '
                                   'stakeholders by themes, products and '
                                   'customers - Beyond kicking off work with '
                                   'engineering many stakeholders want to '
                                   'understand how whys, encoded in key '
                                   'themes, are being\n'
                                   'resolved.  For example customer success '
                                   'managers will need to know how their '
                                   'customers have affected the roadmap, '
                                   'customers themselves would like to '
                                   'understand their level of influence, and\n'
                                   'marketing teams will want to map features '
                                   'to key user pain points.  This means an '
                                   'offer should enable all interested '
                                   'stakeholders to ask and answer key '
                                   'questions beyond the what is needed to '
                                   'drive a roadmap.',
                              '8': 'PRFAQ - In the third round of interviews '
                                   'it has become obvious that the output '
                                   'format should look more like an Amazon '
                                   'PR-FAQ which stands for Press Release and\n'
                                   'Frequently Asked Questions.  Therefore as '
                                   'we progress towards MVP it will be '
                                   'required to change the report format to '
                                   'PR-FAQ.',
                              'text': 'Overall the two phases of the study '
                                      'were well paired. Essentially both the '
                                      'first and second phases illustrated '
                                      'that product managers need tooling that '
                                      'enable them to discern the whys behind '
                                      'an effort leadning to a\n'
                                      'distillation of whats needed to build '
                                      'an offer.  Thus there is an opportunity '
                                      'to build a product enabling product '
                                      'managers (and potentially customer '
                                      'success managers) to reveal insights '
                                      'from interactions with users, partners '
                                      'and competitors\n'
                                      'powering efforts ranging from from '
                                      'product modernization to new product '
                                      'introduction. Further, competitive '
                                      'insights surfaced in the second phase '
                                      'related to Aha!.  These insights showed '
                                      'that Aha! has yet\n'
                                      'to tackle features that automatically '
                                      'and systematically use interactions to '
                                      'reveal the whys and whats behind '
                                      'product roadmaps.  (Note that Aha! is '
                                      'highly relevant to sense competitive '
                                      'intelligence because\n'
                                      'they are the leader in market category '
                                      'of Product Management and Roadmapping '
                                      'tooling.)  While these two phases '
                                      'paired well, a weakness was obvious '
                                      'when the two phases were combined:  An '
                                      'intersection\n'
                                      'between them did not clearly surface.  '
                                      'Therefore a third phase was performed '
                                      'to validate and look for clear '
                                      'couplings between the first two '
                                      'phases.  What follows are some of the '
                                      'key\n'
                                      'opportunities discovered through these '
                                      'three phases followed by discrete '
                                      'sections relating systematically '
                                      'uncovered key themes, snippets '
                                      'associated to key themes, and finally '
                                      'abstracts for related interactions.'}},
 'groups': 'users:studyadmin',
 'id': 'f3eae874b1fba924e81d5963a2bc7752ab8d2acd906bb2944f6243f163a6bf23',
 'iterations': {'1': {'interactions': {'201912151800-Customer Insights-Aha': {'guid': 'd42ba72ab7317dea495dbef9fd7a4b18e220316689059d5ce87134a68033ed6a',
                                                                              'state': 'unsummarized'},
                                       '201912151900-Customer Insights-Aha': {'guid': '2975c26e6ac058eaa6617949e4be59c14ed8da69d49168f2b7e11eedc7ff689c',
                                                                              'state': 'unsummarized'},
                                       '201912152000-Customer Insights-Aha': {'guid': '03d225af95bc8d9ae1af795cae25b1f98afd886d3772e7b56b1899642fdbf8fc',
                                                                              'state': 'unsummarized'},
                                       '201912161800-Customer Insights-Aha': {'guid': '203719812f4d2b7d986f134c81c7e01ff0b7ec0a454351ac020b3fc23ee7209f',
                                                                              'state': 'unsummarized'},
                                       '201912161900-Customer Insights-Aha': {'guid': '9c9703bd9ea5aa58fbec75da5b7a67848a2c69efb34d6b82bdd43f4dca700c1a',
                                                                              'state': 'unsummarized'},
                                       '201912162000-Customer Insights-Aha': {'guid': '440a968c8ec519d046a2064e4c1704307499f013eca6fae639cebdc6a1d31080',
                                                                              'state': 'unsummarized'},
                                       '201912171800-Customer Insights-Aha': {'guid': 'cf22d4ac4c07fa502fdf507237396cc919b99ca6d5e20ede53fc0c65c3657886',
                                                                              'state': 'unsummarized'},
                                       '201912171900-Customer Insights-Aha': {'guid': 'adcdc8c0c4e27ef6617cf61927253473986103662e9b1a0c7e3d0b4c93de41f2',
                                                                              'state': 'unsummarized'},
                                       '201912172000-Customer Insights-Aha': {'guid': '02e5fbd561ae1ab679b793644c5bcf50fb26163623e35c2ff1a76f44f1022a46',
                                                                              'state': 'unsummarized'},
                                       '201912181800-Customer Insights-Aha': {'guid': '29581d790d073ab20b1d7814f6c777944b601d038a59a5a9553f47eb29aa20c7',
                                                                              'state': 'unsummarized'},
                                       '201912181900-Customer Insights-Aha': {'guid': '2599cac8d57cc536b8f46b55f4b90a265af000faf09785aebf37303179dbc61b',
                                                                              'state': 'unsummarized'},
                                       '201912182000-Customer Insights-Aha': {'guid': '70cd002264a60361fcea43bfeb5bca9b6cfc05364b377530581a7317cbad69e4',
                                                                              'state': 'unsummarized'},
                                       '201912191800-Customer Insights-Aha': {'guid': 'a0ec3c225c1b5a6df8444955c56d458b6920a91df7417a4a8b19babfd223401d',
                                                                              'state': 'unsummarized'},
                                       '201912191900-Customer Insights-Aha': {'guid': '167c7dc72ed236c70c165e510de251d635d20116922068e8dc4579d6277e2725',
                                                                              'state': 'unsummarized'},
                                       '201912192000-Customer Insights-Aha': {'guid': 'c812a6f111acfb353ba944f3c536334a1c15fb2663c3dd62ca6e0f78208eaf7f',
                                                                              'state': 'unsummarized'},
                                       '201912201800-Customer Insights-Aha': {'guid': '02e4f0587d9426d4d9aa26d88eff656b35058c250ee58703ecb88e187bc6ca31',
                                                                              'state': 'unsummarized'},
                                       '201912201900-Customer Insights-Aha': {'guid': '7f0b7da04a4919c7bc4a2e676fb916e0cc1465deaeadc9d74008baf28268c74c',
                                                                              'state': 'unsummarized'},
                                       '201912202000-Customer Insights-Aha': {'guid': 'fe57ff2b168359e14950b6f46c45a891494b90651adf784096ecd7d4fdd0f003',
                                                                              'state': 'unsummarized'},
                                       '201912211800-Customer Insights-Aha': {'guid': 'cdb15ae893120080c7cef65f23c0a7f0ed16942077a6b3af7be1f2c6fc8fe63a',
                                                                              'state': 'unsummarized'},
                                       '201912211900-Customer Insights-Aha': {'guid': '60438bac13b7fab03a9d48062b1764ffb627acec94403c0eec79185d6771b448',
                                                                              'state': 'unsummarized'},
                                       '201912212000-Customer Insights-Aha': {'guid': '1255026e832da09862cf55623ea0a78d795aa10a12522860e7720c6e3664de16',
                                                                              'state': 'unsummarized'},
                                       '201912212100-Customer Insights-Aha': {'guid': 'a1049f53de0929252fd6b655be1da37ae9ed27fe44f2814b5f0f9e102b7cabd3',
                                                                              'state': 'unsummarized'}},
                      'state': 'unthemed_unsummarized',
                      'totalInteractions': 22},
                'default': {'interactions': {'201402240930-Customer Insights-HDS': {'guid': '37c5b453fdc2a4074958c3c41f02c2491f9961eafbcdc30a354b586e379a94f4',
                                                                                    'state': 'unsummarized'},
                                             '201402241004-Customer Insights-HDS': {'guid': 'e216d44c6b934beebf1cf58a27030233c3e5e9ea8e5fc457c3003f99dc54efe7',
                                                                                    'state': 'unsummarized'},
                                             '201402250831-Customer Insights-HDS': {'guid': 'bd5b40cb911347abb82bc95c59105e7ea1d3ac48248f0644aa348ab5399bd4d3',
                                                                                    'state': 'unsummarized'},
                                             '201402250915-Customer Insights-HDS': {'guid': '57bf64ca80c491324e917cbeda55d6fe7494c9c8c9e09033a9648e6d4e1cd640',
                                                                                    'state': 'unsummarized'},
                                             '201402270900-Customer Insights-HDS': {'guid': 'af98040145afe692ae78b806323289ad5fddb99c5f45d453d8fc5dde2292a8a9',
                                                                                    'state': 'unsummarized'},
                                             '201402271515-Customer Insights-HDS': {'guid': '0928f03c7b34f90333eacd162fe8ba1dc748639d1cd361613e70de6253222322',
                                                                                    'state': 'unsummarized'},
                                             '201402281310-Customer Insights-HDS': {'guid': '76d41347eba7ddf45aaa7ccf9e40d204e3b0f643ede6d3fc4d212af8c0ffa7de',
                                                                                    'state': 'unsummarized'},
                                             '201403101041-Customer Insights-HDS': {'guid': 'c1eaca9b8de83997b81c2143479b78b5b705c878ef3f1610257278691fdf95d4',
                                                                                    'state': 'unsummarized'},
                                             '201403110945-Customer Insights-HDS': {'guid': '1c992ed623c0ce6ec01470a3438720c39198c0153dcc38be24429a42137dd3be',
                                                                                    'state': 'unsummarized'},
                                             '201403111306-Customer Insights-HDS': {'guid': '1f15ec408b0857662152566408118b580734684f1e7dca5a6d7a77f84cffb041',
                                                                                    'state': 'unsummarized'},
                                             '201403121034-Customer Insights-HDS': {'guid': '60d72cc0a3f0837a81edeec80b8673895ab076d52753d4707115d6f81a239883',
                                                                                    'state': 'unsummarized'},
                                             '201403130801-Customer Insights-HDS': {'guid': '43ac78317d2c402abe0b9afd942e1e742e4029ea3a85679bde2cb740f3c697db',
                                                                                    'state': 'unsummarized'},
                                             '201403140702-Customer Insights-HDS': {'guid': '1fe08d24f23e303d70f73b438b33556df190ee7c2edb076879f9a15f676ee558',
                                                                                    'state': 'unsummarized'}},
                            'state': 'unthemed_unsummarized',
                            'totalInteractions': 13},
                'state': 'unthemed_unsummarized',
                'totalInteractions': 35,
                'totalIterations': 2},
 'keyQuestions': {'1': {'included': True,
                        'notes': 'This relates to the history of current '
                                 'content.',
                        'question': 'Do you know if there are any customer '
                                    'study materials and where you might go to '
                                    'find them?'},
                  '10': {'included': True,
                         'notes': 'Focuses on what outcomes and consumption '
                                  'practices are needed.',
                         'question': 'How do you typically use customer study '
                                     'materials in your plans?'},
                  '11': {'included': True,
                         'notes': 'Focuses on what outcomes and consumption '
                                  'practices are needed.',
                         'question': 'If you do not how do you consolidate '
                                     'your own information to produce release, '
                                     'plan, other content?'},
                  '12': {'included': False,
                         'notes': '',
                         'question': 'Are there other kinds of data to include '
                                     'in conjunction with customer study '
                                     'data/materials, and if so can you '
                                     'describe the data?'},
                  '2': {'included': True,
                        'notes': 'This relates to the history of current '
                                 'content.',
                        'question': 'If you are aware of the materials is the '
                                    'current format sufficient or insufficient '
                                    'for your needs?'},
                  '3': {'included': True,
                        'notes': 'Maps to how a user wants to experiencing the '
                                 'content and collateral.',
                        'question': 'How would you like to explore the '
                                    'materials to get the best possible '
                                    'benefit?'},
                  '4': {'included': True,
                        'notes': 'Maps to how a user wants to experiencing the '
                                 'content and collateral.',
                        'question': 'Do you imagine that some kind of '
                                    'visualization of the findings would be '
                                    'useful/helpful?'},
                  '5': {'included': True,
                        'notes': 'Maps to how a user wants to experiencing the '
                                 'content and collateral.',
                        'question': 'Are you familiar with Word/Tag Clouds and '
                                    'key term visualization, and if so do you '
                                    'think they would be helpful?'},
                  '6': {'included': True,
                        'notes': 'Maps to how a user wants to experiencing the '
                                 'content and collateral.',
                        'question': 'Are specific organization techniques '
                                    'useful or helpful such as content or key '
                                    'term by geography, time, and vertical or '
                                    'sector?  Are there others than those '
                                    'mentioned?'},
                  '7': {'included': True,
                        'notes': 'Maps to how a user wants to experiencing the '
                                 'content and collateral.',
                        'question': 'Do you imagine that you want to get to '
                                    'the content directly or are more '
                                    'summarized abstracts or key term '
                                    'visualizations a better place to start?'},
                  '8': {'included': True,
                        'notes': 'Maps to how a user wants to experiencing the '
                                 'content and collateral.',
                        'question': 'What platform is the best target for such '
                                    'an exploration system?'},
                  '9': {'included': True,
                        'notes': 'Focuses on what outcomes and consumption '
                                 'practices are needed.',
                        'question': 'What kinds of discoveries and findings do '
                                    'you anticipate are possible or even '
                                    'relevant?'}},
 'keyThemeFrequencies': {'1': {'Aha': '37'},
                         '2': {'Aha': '49'},
                         '3': {'Aha': '15'},
                         '4': {'Aha': '14'},
                         '5': {'HDS': '12'},
                         '6': {'HDS': '11'},
                         '7': {'HDS': '8'},
                         '8': {'HDS': '14'},
                         '9': {'HDS': '19'}},
 'keyThemeQuotes': {'1': {'Julia Voynova, Aha': 'Interview recordings is a '
                                                'nice thing to have but '
                                                'honestly I almost never '
                                                'listen to them as it is very '
                                                'time consuming and actually '
                                                'you do not really\n'
                                                'need every single word the '
                                                'customer said.',
                          'Justin Williams, Aha': 'Do not do surveys a lot of '
                                                  'people will be seduced by '
                                                  'their ease and '
                                                  'semi-quantitative nature\n'
                                                  '... but they are almost '
                                                  'NEVER the right tool. Most '
                                                  'orgs would be better off '
                                                  'completely discarding them. '
                                                  '... The 1:1 interview or '
                                                  'user test remains\n'
                                                  'the single best tool for '
                                                  'qualitative learning.'},
                    '2': {'Rich Mironov, Aha': 'So we may choose to keep '
                                               'interview notes in GDrive (or '
                                               'Box or DropBox or SharePoint '
                                               'or iCloud). And presentations '
                                               'for customers wherever our '
                                               'sales\n'
                                               'team has chosen for internal '
                                               'publishing. And financial '
                                               'projections in whatever FP&A '
                                               'application our company has '
                                               'settled on. Product management '
                                               'has\n'
                                               'many functional stakeholders, '
                                               'and chances of any single '
                                               'company wide solution are '
                                               'nearly nil.'},
                    '3': {'Ruby Menon, Aha': 'Thanks, Todd. I did write user '
                                             'personas for 3 types of users we '
                                             'think would be interested in the '
                                             'product. My challenge is that '
                                             'our CEO who is also\n'
                                             'the visionary and product owner '
                                             'identified 3 users from '
                                             'anecdotal vs. actual customer '
                                             'interviews in developing the '
                                             'product.'},
                    '4': {'David Fradin, Aha': 'Start with observing what your '
                                               'prospective customer wants to '
                                               'do, then interview and survey. '
                                               'That will tell you exactly the '
                                               'problem(s) they are\n'
                                               'trying to solve. Then get your '
                                               'designers and development team '
                                               'involved in identifying '
                                               'innovative ways to help them '
                                               'do it faster and better.'},
                    '5': {'Bob OHeir, HDS': 'Uh, I think that one of the key '
                                            'things is what are the customer '
                                            'initiatives. This will help me '
                                            'better frame my products and '
                                            'directions accordingly. Level\n'
                                            'of investment from customers as '
                                            'in budget. Are they taking the '
                                            'time to look at competitors. This '
                                            'will help me determine which '
                                            'requirements are the most\n'
                                            'relevant. These kinds of outputs '
                                            'would be great! It would be '
                                            'better than the current state of '
                                            'affairs where we have to '
                                            'continually go back to the field\n'
                                            'and ask some of these data.'},
                    '6': {'Hitachi Data Systems Product Manager': 'I think I '
                                                                  'use it to '
                                                                  'validate my '
                                                                  'own vision '
                                                                  'and '
                                                                  'strategy. I '
                                                                  'use it to '
                                                                  'validate '
                                                                  'what I’m '
                                                                  'hearing '
                                                                  'from PM, '
                                                                  'sales, OTP, '
                                                                  'customers, '
                                                                  'etc. Given '
                                                                  'all of '
                                                                  'that\n'
                                                                  'I use it to '
                                                                  'defend '
                                                                  'where we’re '
                                                                  'going. '
                                                                  'Here’s '
                                                                  'where we’re '
                                                                  'going and '
                                                                  'this '
                                                                  'matches '
                                                                  'what we see '
                                                                  'with OTP, '
                                                                  'etc. We '
                                                                  'think that '
                                                                  'this is '
                                                                  'super '
                                                                  'valuable '
                                                                  'and\n'
                                                                  'use it to '
                                                                  'reinforce '
                                                                  'directions, '
                                                                  'etc. I '
                                                                  'think that '
                                                                  'the '
                                                                  'customer '
                                                                  'quotes are '
                                                                  'for me the '
                                                                  'most '
                                                                  'valuable. '
                                                                  'The author '
                                                                  'of the doc '
                                                                  'can always '
                                                                  'sort of '
                                                                  'spin it.\n'
                                                                  'At least '
                                                                  'the '
                                                                  'perception '
                                                                  'is that '
                                                                  'they always '
                                                                  'have some '
                                                                  'sort of '
                                                                  'angle. Even '
                                                                  'if I wanted '
                                                                  'to I could '
                                                                  'not '
                                                                  'read/listen '
                                                                  'to the '
                                                                  'materials. '
                                                                  'I think '
                                                                  'that the\n'
                                                                  'mobile '
                                                                  'stuff is a '
                                                                  'little '
                                                                  'ahead of '
                                                                  'its time, '
                                                                  'but maybe '
                                                                  'if you '
                                                                  'started now '
                                                                  'it would be '
                                                                  'ready for '
                                                                  'consumption.'},
                    '7': {'Walter Amsler, HDS': 'Well the example of talking '
                                                'with the analysts helped me '
                                                'to get a lot more clarity in '
                                                'talking about the problem '
                                                'spaces. This helped my '
                                                'understanding\n'
                                                'overall in the market and '
                                                'also allowed me to build '
                                                'contacts in the industry. '
                                                'Further I keep going back to '
                                                'the data to reuse it for '
                                                'validations and\n'
                                                'results. It actually goes two '
                                                'ways because we can share '
                                                'with them some of the great '
                                                'stuff we’re working on which '
                                                'is kind of symbiotic. They '
                                                'feed\n'
                                                'on the data and make it '
                                                'something digestible they can '
                                                'sell in the world.'},
                    '8': {'Aki Harada, HDS': 'Visualization will be very '
                                             'useful, but\n'
                                             'the way that you visualize is '
                                             'highly dependent on who created '
                                             'it. I don’t know how we can '
                                             'create things in a non-uniform '
                                             'way. How can we create\n'
                                             'visuals in different ways? If '
                                             'you want to get a specific '
                                             'answer from the beginning they '
                                             'visualizations are biased. It '
                                             'depends if you’re non-native\n'
                                             'then you may miss the context of '
                                             'the input from audio content. '
                                             'The way that you visualize the '
                                             'data there isn’t an ultimate way '
                                             'to present the data.\n'
                                             'At the same time it is very '
                                             'convincing that you have '
                                             'visuals.',
                          'Rich Rogers, HDS': 'I always tend to think. I used '
                                              'to always tell the team that we '
                                              'should have a knowledge share '
                                              'matrix. I love those documents, '
                                              'but sometimes their\n'
                                              'intimidating. Just wondering if '
                                              'there should be a one page '
                                              'executive summary. Just a one '
                                              'page summary. The content is '
                                              'great, but some kind of exec\n'
                                              'summary might be nice. '
                                              'Sometimes just opening the '
                                              '20-30 page document might be '
                                              'overwhelming.'},
                    '9': {'Charles Hickman, HDS': 'It depends on whether or '
                                                  'not I’m going into an area '
                                                  'I don’t know very well as\n'
                                                  'opposed to this is a topic '
                                                  'I understand and I’m going '
                                                  'to go more grass roots. '
                                                  'Existing market: Bottom up, '
                                                  'Emerging market: top down.',
                          'Scott Nacey, HDS': 'Essentially with key terms '
                                              'which will grow over time. I’d '
                                              'also like to see some '
                                              'visualization such as Wolfram '
                                              'Alpha. Number trending, '
                                              'Frequencies,\n'
                                              'meaning of words. I’d start '
                                              'with the key term library '
                                              'internal data, our written '
                                              'reports, but more importantly '
                                              'being able to get to some of '
                                              'the recorded\n'
                                              'data. I’d be thrilled with '
                                              'that, and it doesn’t have to be '
                                              'perfectly automated. Just '
                                              'having our own stuff searchable '
                                              'and be able to search the '
                                              'audio\n'
                                              'content would be huge. Very '
                                              'seldom will the audio content '
                                              'be high fidelity. Sometimes '
                                              'there are follow-up discussions '
                                              'that are followed by another '
                                              'team\n'
                                              '[PM, Eng, Sales] and we don’t '
                                              'see the connection between '
                                              'these studies, yet in some '
                                              'cases we don’t even follow-up. '
                                              'Also we don’t get cold calls '
                                              'and we\n'
                                              'miss customers that we don’t '
                                              'have or haven’t acquired.'}},
 'keyThemes': {'1': {'description': 'A consistent approach to performing '
                                    'stakeholder, user and competitive '
                                    'interviews',
                     'frequency': '37',
                     'name': 'Standard Interview Process'},
               '2': {'description': 'Provide a common set of tooling the '
                                    'enables a standard interview process',
                     'frequency': '49',
                     'name': 'Standard Interview Tooling'},
               '3': {'description': 'An approach to generating and maintaining '
                                    'personas from your audience',
                     'frequency': '15',
                     'name': 'Managing Personas'},
               '4': {'description': 'Where and how to capture key ideas for an '
                                    'offer',
                     'frequency': '14',
                     'name': 'Product Idea Sources'},
               '5': {'description': 'What can and should be done with output '
                                    'from customer and competitive research',
                     'frequency': '12',
                     'name': 'Requirements and Planning'},
               '6': {'description': 'Other uses for customer and competitive '
                                    'insights be used',
                     'frequency': '11',
                     'name': 'Personal Strategy'},
               '7': {'description': 'Another usage scenario for customer and '
                                    'competitive insight',
                     'frequency': '8',
                     'name': 'Concept Validation'},
               '8': {'description': 'How to access and experience insight '
                                    'content',
                     'frequency': '14',
                     'name': 'Abstract to Detailed'},
               '9': {'description': 'What the most important approach is to '
                                    'analysis of insight collateral',
                     'frequency': '19',
                     'name': 'Key-Term Analysis'}},
 'linkedCompanies': {'Aha': '6dbfa33b06706033931b0154210fbcb5fafb995315eccfbd8bc5b12d5e5569f7',
                     'HDS': 'b61e57adaaa834f2a560be1b8d1b62c0ebbfd68cb3d33917185bc1792063a677'},
 'linkedInteractions': {'201402240930-Customer Insights-HDS': '37c5b453fdc2a4074958c3c41f02c2491f9961eafbcdc30a354b586e379a94f4',
                        '201402241004-Customer Insights-HDS': 'e216d44c6b934beebf1cf58a27030233c3e5e9ea8e5fc457c3003f99dc54efe7',
                        '201402250831-Customer Insights-HDS': 'bd5b40cb911347abb82bc95c59105e7ea1d3ac48248f0644aa348ab5399bd4d3',
                        '201402250915-Customer Insights-HDS': '57bf64ca80c491324e917cbeda55d6fe7494c9c8c9e09033a9648e6d4e1cd640',
                        '201402270900-Customer Insights-HDS': 'af98040145afe692ae78b806323289ad5fddb99c5f45d453d8fc5dde2292a8a9',
                        '201402271515-Customer Insights-HDS': '0928f03c7b34f90333eacd162fe8ba1dc748639d1cd361613e70de6253222322',
                        '201402281310-Customer Insights-HDS': '76d41347eba7ddf45aaa7ccf9e40d204e3b0f643ede6d3fc4d212af8c0ffa7de',
                        '201403101041-Customer Insights-HDS': 'c1eaca9b8de83997b81c2143479b78b5b705c878ef3f1610257278691fdf95d4',
                        '201403110945-Customer Insights-HDS': '1c992ed623c0ce6ec01470a3438720c39198c0153dcc38be24429a42137dd3be',
                        '201403111306-Customer Insights-HDS': '1f15ec408b0857662152566408118b580734684f1e7dca5a6d7a77f84cffb041',
                        '201403121034-Customer Insights-HDS': '60d72cc0a3f0837a81edeec80b8673895ab076d52753d4707115d6f81a239883',
                        '201403130801-Customer Insights-HDS': '43ac78317d2c402abe0b9afd942e1e742e4029ea3a85679bde2cb740f3c697db',
                        '201403140702-Customer Insights-HDS': '1fe08d24f23e303d70f73b438b33556df190ee7c2edb076879f9a15f676ee558',
                        '201912151800-Customer Insights-Aha': 'd42ba72ab7317dea495dbef9fd7a4b18e220316689059d5ce87134a68033ed6a',
                        '201912151900-Customer Insights-Aha': '2975c26e6ac058eaa6617949e4be59c14ed8da69d49168f2b7e11eedc7ff689c',
                        '201912152000-Customer Insights-Aha': '03d225af95bc8d9ae1af795cae25b1f98afd886d3772e7b56b1899642fdbf8fc',
                        '201912161800-Customer Insights-Aha': '203719812f4d2b7d986f134c81c7e01ff0b7ec0a454351ac020b3fc23ee7209f',
                        '201912161900-Customer Insights-Aha': '9c9703bd9ea5aa58fbec75da5b7a67848a2c69efb34d6b82bdd43f4dca700c1a',
                        '201912162000-Customer Insights-Aha': '440a968c8ec519d046a2064e4c1704307499f013eca6fae639cebdc6a1d31080',
                        '201912171800-Customer Insights-Aha': 'cf22d4ac4c07fa502fdf507237396cc919b99ca6d5e20ede53fc0c65c3657886',
                        '201912171900-Customer Insights-Aha': 'adcdc8c0c4e27ef6617cf61927253473986103662e9b1a0c7e3d0b4c93de41f2',
                        '201912172000-Customer Insights-Aha': '02e5fbd561ae1ab679b793644c5bcf50fb26163623e35c2ff1a76f44f1022a46',
                        '201912181800-Customer Insights-Aha': '29581d790d073ab20b1d7814f6c777944b601d038a59a5a9553f47eb29aa20c7',
                        '201912181900-Customer Insights-Aha': '2599cac8d57cc536b8f46b55f4b90a265af000faf09785aebf37303179dbc61b',
                        '201912182000-Customer Insights-Aha': '70cd002264a60361fcea43bfeb5bca9b6cfc05364b377530581a7317cbad69e4',
                        '201912191800-Customer Insights-Aha': 'a0ec3c225c1b5a6df8444955c56d458b6920a91df7417a4a8b19babfd223401d',
                        '201912191900-Customer Insights-Aha': '167c7dc72ed236c70c165e510de251d635d20116922068e8dc4579d6277e2725',
                        '201912192000-Customer Insights-Aha': 'c812a6f111acfb353ba944f3c536334a1c15fb2663c3dd62ca6e0f78208eaf7f',
                        '201912201800-Customer Insights-Aha': '02e4f0587d9426d4d9aa26d88eff656b35058c250ee58703ecb88e187bc6ca31',
                        '201912201900-Customer Insights-Aha': '7f0b7da04a4919c7bc4a2e676fb916e0cc1465deaeadc9d74008baf28268c74c',
                        '201912202000-Customer Insights-Aha': 'fe57ff2b168359e14950b6f46c45a891494b90651adf784096ecd7d4fdd0f003',
                        '201912211800-Customer Insights-Aha': 'cdb15ae893120080c7cef65f23c0a7f0ed16942077a6b3af7be1f2c6fc8fe63a',
                        '201912211900-Customer Insights-Aha': '60438bac13b7fab03a9d48062b1764ffb627acec94403c0eec79185d6771b448',
                        '201912212000-Customer Insights-Aha': '1255026e832da09862cf55623ea0a78d795aa10a12522860e7720c6e3664de16',
                        '201912212100-Customer Insights-Aha': 'a1049f53de0929252fd6b655be1da37ae9ed27fe44f2814b5f0f9e102b7cabd3'},
 'public': False,
 'questions': {'default': {'questions': {'1': {'included': True,
                                               'notes': 'This relates to the '
                                                        'history of current '
                                                        'content.',
                                               'question': 'Do you know if '
                                                           'there are any '
                                                           'customer study '
                                                           'materials and '
                                                           'where you might go '
                                                           'to find them?'},
                                         '10': {'included': True,
                                                'notes': 'Focuses on what '
                                                         'outcomes and '
                                                         'consumption '
                                                         'practices are '
                                                         'needed.',
                                                'question': 'How do you '
                                                            'typically use '
                                                            'customer study '
                                                            'materials in your '
                                                            'plans?'},
                                         '11': {'included': True,
                                                'notes': 'Focuses on what '
                                                         'outcomes and '
                                                         'consumption '
                                                         'practices are '
                                                         'needed.',
                                                'question': 'If you do not how '
                                                            'do you '
                                                            'consolidate your '
                                                            'own information '
                                                            'to produce '
                                                            'release, plan, '
                                                            'other content?'},
                                         '12': {'included': False,
                                                'notes': '',
                                                'question': 'Are there other '
                                                            'kinds of data to '
                                                            'include in '
                                                            'conjunction with '
                                                            'customer study '
                                                            'data/materials, '
                                                            'and if so can you '
                                                            'describe the '
                                                            'data?'},
                                         '2': {'included': True,
                                               'notes': 'This relates to the '
                                                        'history of current '
                                                        'content.',
                                               'question': 'If you are aware '
                                                           'of the materials '
                                                           'is the current '
                                                           'format sufficient '
                                                           'or insufficient '
                                                           'for your needs?'},
                                         '3': {'included': True,
                                               'notes': 'Maps to how a user '
                                                        'wants to experiencing '
                                                        'the content and '
                                                        'collateral.',
                                               'question': 'How would you like '
                                                           'to explore the '
                                                           'materials to get '
                                                           'the best possible '
                                                           'benefit?'},
                                         '4': {'included': True,
                                               'notes': 'Maps to how a user '
                                                        'wants to experiencing '
                                                        'the content and '
                                                        'collateral.',
                                               'question': 'Do you imagine '
                                                           'that some kind of '
                                                           'visualization of '
                                                           'the findings would '
                                                           'be '
                                                           'useful/helpful?'},
                                         '5': {'included': True,
                                               'notes': 'Maps to how a user '
                                                        'wants to experiencing '
                                                        'the content and '
                                                        'collateral.',
                                               'question': 'Are you familiar '
                                                           'with Word/Tag '
                                                           'Clouds and key '
                                                           'term '
                                                           'visualization, and '
                                                           'if so do you think '
                                                           'they would be '
                                                           'helpful?'},
                                         '6': {'included': True,
                                               'notes': 'Maps to how a user '
                                                        'wants to experiencing '
                                                        'the content and '
                                                        'collateral.',
                                               'question': 'Are specific '
                                                           'organization '
                                                           'techniques useful '
                                                           'or helpful such as '
                                                           'content or key '
                                                           'term by geography, '
                                                           'time, and vertical '
                                                           'or sector?  Are '
                                                           'there others than '
                                                           'those mentioned?'},
                                         '7': {'included': True,
                                               'notes': 'Maps to how a user '
                                                        'wants to experiencing '
                                                        'the content and '
                                                        'collateral.',
                                               'question': 'Do you imagine '
                                                           'that you want to '
                                                           'get to the content '
                                                           'directly or are '
                                                           'more summarized '
                                                           'abstracts or key '
                                                           'term '
                                                           'visualizations a '
                                                           'better place to '
                                                           'start?'},
                                         '8': {'included': True,
                                               'notes': 'Maps to how a user '
                                                        'wants to experiencing '
                                                        'the content and '
                                                        'collateral.',
                                               'question': 'What platform is '
                                                           'the best target '
                                                           'for such an '
                                                           'exploration '
                                                           'system?'},
                                         '9': {'included': True,
                                               'notes': 'Focuses on what '
                                                        'outcomes and '
                                                        'consumption practices '
                                                        'are needed.',
                                               'question': 'What kinds of '
                                                           'discoveries and '
                                                           'findings do you '
                                                           'anticipate are '
                                                           'possible or even '
                                                           'relevant?'}},
                           'totalQuestions': 12},
               'totalIterations': 1,
               'totalQuestions': 12},
 'studyName': 'Customer Insights',
 'totalCompanies': 2,
 'totalInteractions': 35,
 'totalKeyQuestions': 12,
 'totalKeyThemes': 9}
```
## update_companies.py - this is a work in progress and is not guaranteed to work at this stage
```
usage: update_companies [-h] [--rest_url REST_URL] --guid GUID [--set_interactions_state {processing,summarized,unsummarized}] [--set_iteration_state {processing,summarized,unsummarized,themed,unthemed}]
                        [--set_container_state CONTAINER_STATE] [--set_property PROPERTY] [--user USER] [--secret SECRET]

A mediumroast.io example utility that updates company properties using mr_api.

optional arguments:
  -h, --help            show this help message and exit
  --rest_url REST_URL   The URL of the target REST server
  --guid GUID           Specify the GUID of the object to operate on
  --set_interactions_state {processing,summarized,unsummarized}
                        Set the state of a company's interactions
  --set_iteration_state {processing,summarized,unsummarized,themed,unthemed}
                        Set the state of the iteration
  --set_container_state CONTAINER_STATE
                        Set the state of the iteration's container
  --set_property PROPERTY
                        Set an arbitrary property for the company using well formed JSON
  --user USER           User name
  --secret SECRET       Secret or password
```
## update_interactions.py
```
usage: update_interactions [-h] [--rest_url REST_URL] --guid GUID [--set_state {processing,summarized,unsummarized}] [--set_all_state {processing,summarized,unsummarized}] [--set_summary SUMMARY] [--set_property PROPERTY]
                           [--user USER] [--secret SECRET]

A mediumroast.io example utility that updates interaction properties using mr_api.

optional arguments:
  -h, --help            show this help message and exit
  --rest_url REST_URL   The URL of the target REST server
  --guid GUID           Specify the GUID of the object to operate on
  --set_state {processing,summarized,unsummarized}
                        Set the state of the interaction
  --set_all_state {processing,summarized,unsummarized}
                        Set the state of all interactions
  --set_summary SUMMARY
                        Set the abstract/summary of the interaction
  --set_property PROPERTY
                        Set an arbitrary property for the interaction using well formed JSON
  --user USER           User name
  --secret SECRET       Secret or password
```
