__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-27'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import configparser as conf
import random
from datetime import datetime

# Perform local imports
from mr_python.helpers import studies
from mr_python.helpers import interactions
from mr_python.helpers import companies
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

        create_objects()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__(self, rewrite_rule_dir, debug=False):
        # TODO consume the additional defaults for URL, etc.
        self.RAW_COMPANY_NAME = 7
        self.RAW_STUDY_NAME = 6
        self.RAW_DATE = 0
        self.REGION = 1
        self.COUNTRY = 2
        self.STATE_PROVINCE = 3
        self.CITY = 4
        self.URL = 9
        self.THUMBNAIL = 10
        self.DATETIME = 0
        self.RULES = {
            'dir': rewrite_rule_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }

        # This imports the local utilies from mr_sdk for Python
        self.util = utilities()

        # Get the config file
        [success, status, self.rules] = self.util.get_config_file(self.RULES['dir'] + '/' + self.RULES['interaction'])

        # Set debug to true or false
        self.debug = debug

        # TODO Update for this object type and put into the various helper methods.  This is wrong as of now
        # Specify what to skip when processing sections in the conf file
        self.to_skip = r"^description|groups|security_scope|substudies|substudy_definition|substudy_type"

    # TODO rewrite this to follow the load_studies utility

    def _transform_interaction(self, interaction_name):
        """Internal method to rewrite or augment key aspects of an interaction object as per definitions in the configuration file."""


        # Add the items which are either rewritten or not present in the file_name metadata.
        groups = self.rules['groups'][interaction_name] if interaction_name in self.rules['groups'] else self.rules['DEFAULT']['groups']

        abstract = self.rules['abstracts'][interaction_name] if interaction_name in self.rules['abstracts'] else self.rules['DEFAULT']['abstract']

        status = self.rules['statuses'][interaction_name] if interaction_name in self.rules['statuses'] else self.rules['DEFAULT']['status']

        interaction_type = self.rules['types'][interaction_name] if interaction_name in self.rules['types'] else self.rules['DEFAULT']['type']

        contact_address = self.rules['contact_addresses'][interaction_name] if interaction_name in self.rules['contact_addresses'] else self.rules['DEFAULT']['contact_address']

        contact_zipPostal = self.rules['contact_zipPostals'][interaction_name] if interaction_name in self.rules['contact_zipPostals'] else self.rules['DEFAULT']['contact_zipPostal']

        contact_phone = self.rules['contact_phones'][interaction_name] if interaction_name in self.rules['contact_phones'] else self.rules['DEFAULT']['contact_phone']

        contact_linkedin = self.rules['contact_linkedins'][interaction_name] if interaction_name in self.rules['contact_linkedins'] else self.rules['DEFAULT']['contact_linkedin']

        contact_email = self.rules['contact_emails'][interaction_name] if interaction_name in self.rules['contact_emails'] else self.rules['DEFAULT']['contact_email']

        contact_twitter = self.rules['contact_twitters'][interaction_name] if interaction_name in self.rules['contact_twitters'] else self.rules['DEFAULT']['contact_twitter']

        contact_name = self.rules['contact_names'][interaction_name] if interaction_name in self.rules['contact_names']else self.rules['DEFAULT']['contact_name']

        security_scope = self.rules['security_scopes'][interaction_name] if interaction_name in self.rules['security_scopes'] else self.rules['DEFAULT']['security_scope']
            
        security_scope = True if security_scope == 'True' else False

        return {'groups': groups,
                'abstract': abstract,
                'status': status,
                'interactionType': interaction_type,
                'contactAddress': contact_address,
                'contactZipPostal': contact_zipPostal,
                'contactPhone': contact_phone,
                'contactLinkedIn': contact_linkedin,
                'contactEmail': contact_email,
                'contactTwitter': contact_twitter,
                'contactName': contact_name,
                'public': security_scope}

    def _get_status(self, range=4):
        """An internal method to compute a random status to drive UX functionality
        """
        idx = random.randrange(0, range)
        statuses = ['Completed', 'Scheduled', 'Canceled', 'Planned', 'Unknown']
        return idx

    def create_objects(self, raw_objects, file_output=True):
        """Create study objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all company objects and the total number of company objects processed
        """
        final_objects = {
            'totalInteractions': 0,
            'interactions': []
        }

        # Temp storage for objects
        tmp_objects = {}

        for object in raw_objects:

            # Capture the right study_name and then fetch the study's ID
            study_xform = studies(rewrite_config_dir=self.RULES['dir'])
            study_name = study_xform.get_name(object[self.RAW_STUDY_NAME])
            study_id = study_xform.make_id(study_name)

            # Capture the right company_name and then fetch the study's ID
            company_xform = companies(rewrite_config_dir=self.RULES['dir'])
            company_name = company_xform.get_name(
                object[self.RAW_COMPANY_NAME])
            company_id = company_xform.make_id(company_name)

            # Perform basic transformation of company data based upon data in the configuration file
            interaction_xform = interactions(self.RULES['dir'])
            interaction_name = interaction_xform.get_name(
                object[self.RAW_DATE], study_name, company_name)
            interaction_obj = self._transform_interaction(interaction_name)
            interaction_date, interaction_time = self.util.correct_date(
                object[self.DATETIME])

            # Set the specific dates for the interaction
            interaction_creation = datetime.now().isoformat()
            year = int(interaction_date[0:4])
            month = int(interaction_date[4:6])
            day = int(interaction_date[6:8])
            hour = int(interaction_time[0:2])
            minute = int(interaction_time[2:3])
            interaction_date_time = datetime(year, month, day, hour=hour, minute=minute).isoformat()

            # TODO the date needs to be fixed potentially with the helper functions included
            # TODO this is only partially implemented and needs to be looked at again
            if tmp_objects.get(interaction_name) == None:
                long_lat = self.util.locate(
                    object[self.CITY] + ',' + object[self.STATE_PROVINCE] + ',' + object[self.COUNTRY])
                tmp_objects[interaction_name] = {
                    "creator_id":1, # TODO it is a bug if this is required
                    "owner_id": 1, # TODO it is a bug if this is required
                    "name": interaction_name,
                    "description": interaction_xform.get_description(company_name, study_name),
                    "creation_date": interaction_creation,
                    "modification_date": interaction_creation,
                    "date_time": interaction_date_time,
                    "public": interaction_obj['public'],
                    "groups": 'user:studyadmin',
                    "longitude": long_lat[0],
                    "latitude": long_lat[1],
                    "contact_name": interaction_obj['contactName'],
                    "contact_email": interaction_obj['contactEmail'],
                    "contact_linkedin": interaction_obj['contactLinkedIn'],
                    "contact_twitter": interaction_obj['contactTwitter'],
                    "url": object[self.URL],
                    "city": object[self.CITY],
                    "street_address": interaction_obj['contactAddress'],
                    "zip_postal": interaction_obj['contactZipPostal'],
                    "state_province": object[self.STATE_PROVINCE],
                    "country": object[self.COUNTRY],
                    "region": object[self.REGION],
                    "phone": interaction_obj['contactPhone'],
                    "interaction_type": 1, # TODO this should be transformed to a string
                    "status": self._get_status(), # NOTE this is remedied as the status can range from 0 - 4
                    "abstract": interaction_obj['abstract'],
                    "thumbnail": object[self.THUMBNAIL] # TODO this is deprecated
                    # "state": "unsummarized", # TODO the state variable is needed should be boolean associated to abstract state
                    # "linkedStudies": {study_name: study_id}, # TODO verify implementation
                    # "linkedCompanies": {company_name: company_id}, # TODO verify implementation    
                }
            # TODO resolve how to fix linked interactions, this isn't supported for now
            # else:
            #     tmp_objects[interaction_name]["linkedStudies"][study_name] = study_id
            #     tmp_objects[interaction_name]["linkedCompanies"][company_name] = company_id

        # TODO Look at the company.py obj and fix accordingly 
        for interaction in tmp_objects.keys():
            # if file_output:
            #     # Generally the model to create a GUID is to hash the name and the description for all objects.
            #     # We will only use this option when we're outputing to a file.
            #     guid = self.util.hash_it(
            #         interaction + tmp_objects[interaction]['description'])
            #     tmp_objects[interaction]['GUID'] = guid
            #     tmp_objects[interaction]['id'] = guid

            final_objects['interactions'].append(tmp_objects[interaction])

        return final_objects
