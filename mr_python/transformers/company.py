__version__ = '2.0'
__author__ = "Michael Hay"
__date__ = '2022-June-25'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

import re
import configparser as conf
from mr_python.helpers import interactions
from mr_python.helpers import studies
from mr_python.helpers import utilities


class Transform:
    """Perform transformation of input data into a proper company object.

    Returns:
        list: A list of dicts which can be pass along to additional 

    Methods:
        get_description()
            Lookup a company description from the configuration file and return it.

        get_industry()
            Lookup a company industry from the configuration file and return it.

        get_name()
            Lookup a company from the configuration file and return it.

        make_id()
            Create a unique company identifier if needed.

        create_objects()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__(self, rewrite_rule_dir, debug=False):
        self.RAW_COMPANY_NAME = 7
        self.RAW_STUDY_NAME = 6
        self.RAW_DATE = 0
        self.REGION = 1
        self.COUNTRY = 2
        self.STATE_PROVINCE = 3
        self.CITY = 4
        self.RULES = {
            'dir': rewrite_rule_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }

        # This imports the local utilies from mr_sdk for Python
        self.util = utilities()

        # Get the config file
        [success, status, self.rules] = self.util.get_config_file(self.RULES['dir'] + '/' + self.RULES['company'])

        # Set debug to true or false
        self.debug = debug

        # TODO Update for this object type and put into the various helper methods.  This is wrong as of now
        # Specify what to skip when processing sections in the conf file
        self.to_skip = r"^description|groups|security_scope|substudies|substudy_definition|substudy_type"

    def _transform_company(self, company_name, extended_rewrite=True):
        """Internal method to rewrite or augment key aspects of a company object as per definitions in the configuration file."""

        # TODO cleanup according to interaction.py
    

        # Add the items which are either rewritten or not present in the file_name metadata.
        # (A)
        industry = self.rules['industries'][company_name] if self.rules['industries'][company_name] else self.rules['DEFAULT']['industry']
        
        role = self.rules.get('roles', company_name) if self.rules.has_option(
            'roles', company_name) else self.rules.get('DEFAULT', 'role')
        description = self.rules.get('descriptions', company_name) if self.rules.has_option(
            'descriptions', company_name) else self.rules.get('DEFAULT', 'description')
        url = self.rules.get('urls', company_name) if self.rules.has_option(
            'urls', company_name) else self.rules.get('DEFAULT', 'url')
        cik = self.rules.get('ciks', company_name) if self.rules.has_option(
            'ciks', company_name) else self.rules.get('DEFAULT', 'cik')
        stockSymbol = self.rules.get('stockSymbols', company_name) if self.rules.has_option(
            'stockSymbols', company_name) else self.rules.get('DEFAULT', 'stockSymbol')
        recent10kURL = self.rules.get('recent10kURLs', company_name) if self.rules.has_option(
            'recent10kURLs', company_name) else self.rules.get('DEFAULT', 'recent10kURL')
        recent10qURL = self.rules.get('recent10qURLs', company_name) if self.rules.has_option(
            'recent10qURLs', company_name) else self.rules.get('DEFAULT', 'recent10qURL')
        phone = self.rules.get('phones', company_name) if self.rules.has_option(
            'phones', company_name) else self.rules.get('DEFAULT', 'phone')

        zipPostal = self.rules.get('zipPostals', company_name) if self.rules.has_option(
            'zipPostals', company_name) else self.rules.get('DEFAULT', 'zipPostal')

        # Should we want to have inputs totally worked through the configuration file we can set up the rewrite logic to look for
        # an extended_rewrite.  This will then create all of the fields which are normally pulled in through the file_name metadata,
        # in addition to the ones not included with the file metadata.
        if extended_rewrite:
            stateProvince = self.rules.get('stateProvinces', company_name) if self.rules.has_option(
                'stateProvinces', company_name) else self.rules.get('DEFAULT', 'stateProvince')
            city = self.rules.get('cities', company_name) if self.rules.has_option(
                'cities', company_name) else self.rules.get('DEFAULT', 'city')
            country = self.rules.get('countries', company_name) if self.rules.has_option(
                'countries', company_name) else self.rules.get('DEFAULT', 'country')
            region = self.rules.get('regions', company_name) if self.rules.has_option(
                'regions', company_name) else self.rules.get('DEFAULT', 'region')
            latitude = self.rules.get('latitudes', company_name) if self.rules.has_option(
                'latitudes', company_name) else self.rules.get('DEFAULT', 'latitude')
            longitude = self.rules.get('longitudes', company_name) if self.rules.has_option(
                'longitudes', company_name) else self.rules.get('DEFAULT', 'longitude')
            country = self.rules.get('countries', company_name) if self.rules.has_option(
                'countries', company_name) else self.rules.get('DEFAULT', 'country')
            streetAddress = self.rules.get('streetAddresses', company_name) if self.rules.has_option(
                'streetAddresses', company_name) else self.rules.get('DEFAULT', 'streetAddress')
            logo = self.rules.get('logos', company_name) if self.rules.has_option(
                'logos', company_name) else self.rules.get('DEFAULT', 'logo')
 
            return {'name': company_name,
                    'role': role,
                    'industry': industry,
                    'description': description,
                    'url': url,
                    'country': country,
                    'cik': cik,
                    'stockSymbol': stockSymbol,
                    'recent10kURL': recent10kURL,
                    'recent10qURL': recent10qURL,
                    'latitude': latitude,
                    'longitude': longitude,
                    'stateProvince': stateProvince,
                    'city': city,
                    'region': region,
                    'phone': phone,
                    'streetAddress': streetAddress,
                    'logo': logo,
                    'zipPostal': zipPostal}
        else:
            return {'name': company_name,
                    'role': role,
                    'industry': industry,
                    'description': description,
                    'url': url,
                    'cik': cik,
                    'stockSymbol': stockSymbol,
                    'recent10kURL': recent10kURL,
                    'recent10qURL': recent10qURL,
                    'phone': phone,
                    'zipPostal': zipPostal}

    #############################################################################################
    # All methods to create a company's document which include:
    #   - Introduction
    #   - Purpose
    #   - Actions
    #############################################################################################
    # INTERNAL METHODS AND HELPER FUNCTIONS

    def _reformat_name(self, study_name, separator='_'):
        """Internal method to reformat the company name by replacing spaces with the separator."""
        return study_name.replace(' ', separator)

    # Transform either default or study specific document elements into the proper data structure
    def _document_helper(self, section, seperator='_'):
        intro = 'Introduction'
        prps = 'Purpose'
        acts = 'Action'
        document = {
            intro: '',
            prps: {},
            acts: {}
        }
        introduction = re.compile('^Introduction', re.IGNORECASE)
        purpose = re.compile('^Purpose', re.IGNORECASE)
        actions = re.compile('^Action_', re.IGNORECASE)
        for idx in list(self.rules[section]):
            if introduction.match(idx):
                document[intro] = self.rules[section][idx]
            elif purpose.match(idx):
                document[prps] = self.rules[section][idx]
            elif actions.match(idx):
                item_type = idx.split(seperator)[1]
                if item_type == 'Text':
                    document['Action']['text'] = self.rules[section][idx]
                else:
                    document['Action'][item_type] = self.rules[section][idx]
        return document

    def _replace_company(self, text, company_name):
        text = text.strip()
        text = text.replace('\n', ' ')
        text = text.replace('$COMPANY$', company_name)
        return text

    def _get_document(self, company_name, default='DEFAULT_PRFAQ'):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        section = self._reformat_name(company_name) + '_PRFAQ'
        document = self._document_helper(section) if self.rules.has_section(
            section) else self._document_helper(default)
        for doc_section in document.keys():
            my_text = document[doc_section]
            if type(my_text) is dict:
                for entry in my_text:
                    local_text = my_text[entry]
                    local_text = self._replace_company(local_text, company_name)
                    my_text[entry] = local_text
            else:
                my_text = self._replace_company(my_text, company_name)
            
            document[doc_section] = my_text
        return document

    def create_objects(self, raw_objects, file_output=True):
        """Create company objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all company objects and the total number of company objects processed
        """
        final_objects = {
            'companies': []
        }

        # Construct objects
        interaction_xform = interactions(self.RULES['dir'])
        study_xform = studies(rewrite_config_dir=self.RULES['dir'])

        # Temp storage for objects
        tmp_objects = {}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            company_obj = self._transform_company(
                object[self.RAW_COMPANY_NAME])


            # Capture the right study_name and then fetch the study's ID
            study_name = study_xform.get_name(object[self.RAW_STUDY_NAME])
            study_id = study_xform.make_id(study_name)

            # Capture the right study_name and then fetch the study's ID
            interaction_name = interaction_xform.get_name(
                object[self.RAW_DATE], study_name, company_obj['name'])
            interaction_id = interaction_xform.make_id(
                object[self.RAW_DATE], company_obj['name'], study_name)

            if tmp_objects.get(object[self.RAW_COMPANY_NAME]) == None:
                long_lat = self.util.locate(
                    object[self.CITY] + ',' + object[self.STATE_PROVINCE] + ',' + object[self.COUNTRY])
                tmp_objects[object[self.RAW_COMPANY_NAME]] = {
                    "name": company_obj['name'],
                    "industry": company_obj['industry'],
                    "role": company_obj['role'],
                    "url": company_obj['url'],
                    "logo_url": company_obj['logo'],
                    "icon": company_obj['logo'],
                    "street_address": company_obj['streetAddress'],
                    "city": object[self.CITY],
                    "state_province": object[self.STATE_PROVINCE],
                    "country": object[self.COUNTRY],
                    "region": object[self.REGION],
                    "phone": company_obj['phone'],
                    "description": company_obj['description'],
                    "cik": company_obj['cik'],
                    "stock_symbol": company_obj['stockSymbol'],
                    "recent10k_url": company_obj['recent10kURL'],
                    "recent10q_url": company_obj['recent10qURL'],
                    "zip_postal": company_obj['zipPostal'],
                    "linked_studies": {study_name: study_id},
                    "linked_interactions": {interaction_name: interaction_id},
                    "longitude": long_lat[0],
                    "latitude": long_lat[1],
                    "document": self._get_document(company_obj['name']),
                }
            else:
                tmp_objects[object[self.RAW_COMPANY_NAME]
                            ]["linked_studies"][study_name] = study_id
                tmp_objects[object[self.RAW_COMPANY_NAME]
                            ]["linked_interactions"][interaction_name] = interaction_id

        for company in tmp_objects.keys():
            # TODO we need to reconcile a local UID with the IDs that the backend supplies.
            #       This would suggest a three step process of identifying the UIDs locally, 
            #       getting the IDs from the backend, and then reconciling as needed.
            # if file_output:
                # Generally the model to create a GUID is to hash the name and the description for all objects.
                # We will only use this option when we're outputing to a file.
                # tmp_objects[company]['GUID'] = self.util.hash_it(
                #     str(company) + str(tmp_objects[company]['description']))
            final_objects['companies'].append(tmp_objects[company])

        return final_objects
