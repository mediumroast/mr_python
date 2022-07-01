__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-27'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import random
from datetime import datetime

# Perform local imports
from .helpers import InteractionHelpers as interactions
from .helpers import CompanyHelpers as companies
from .helpers import StudyHelpers as studies
from mr_python.helpers import utilities

class Transform:
    """Perform the core transformation of input data into a proper interaction object.

    Using the transformation rules written into the rules files specified in 'rewrite_rule_dir'
    create more complete interaction objects which can then be ingested into the backend. This
    kind of transformation can be used from any input like files, file systems and S3 compatible
    object stores where the source data can be massaged into a the following array of arrays.

    '
        [
            [RAW_DATE, REGION, COUNTRY, STATE_PROVINCE, CITY, INDUSTRY, RAW_STUDY_NAME, RAW_COMPANY_NAME, INTERACTION_TYPE, URL],
            ...
            [RAW_DATE, REGION, COUNTRY, STATE_PROVINCE, CITY, INDUSTRY, RAW_STUDY_NAME, RAW_COMPANY_NAME, INTERACTION_TYPE, URL]
        ]
    '

    This input is passed to `create_objects` which in turn generates a dict that contains a list of the interaction objects
    and associated metadata.  (Note, that at this time the metadata is still under construction and the documentation will
    be updated when ready.)  These interaction objects can then be iterated over and ingested into the backend.
    """

    def __init__(self, rewrite_rule_dir, debug=False):
        self.RAW_COMPANY_NAME = 7
        self.RAW_STUDY_NAME = 6
        self.RAW_DATE = 0
        self.REGION = 1
        self.COUNTRY = 2
        self.STATE_PROVINCE = 3
        self.CITY = 4
        self.URL = 9
        self.DATETIME = 0
        self.RULE_DIR = rewrite_rule_dir

        # This imports the local utilies from mr_sdk for Python
        self.util = utilities()

        # Set debug to true or false
        self.debug = debug

    def _transform_interaction(self, interaction_name, xform):
        """Internal method to rewrite or augment key aspects of an interaction object as per definitions in the configuration file."""

        # Add the items which are either rewritten or not present in the file_name metadata.
        groups = xform.get_from_section(interaction_name, 'groups', 'groups')
        abstract = xform.get_from_section(interaction_name, 'abstracts', 'abstract')
        status = xform.get_from_section(interaction_name, 'statuses', 'status')
        interaction_type = xform.get_from_section(interaction_name, 'types', 'type')
        contact_address = xform.get_from_section(interaction_name, 'contact_addresses', 'contact_address')
        contact_zip_postal = xform.get_from_section(interaction_name, 'contact_zip_postals', 'contact_zip_postal')
        contact_phone = xform.get_from_section(interaction_name, 'contact_phones', 'contact_phone')
        contact_linkedin = xform.get_from_section(interaction_name, 'contact_linkedins', 'contact_linkedin')
        contact_email  = xform.get_from_section(interaction_name, 'contact_emails', 'contact_email')
        contact_twitter = xform.get_from_section(interaction_name, 'contact_twitters', 'contact_twitter')
        contact_name = xform.get_from_section(interaction_name, 'contact_names', 'contact_name')
        security_scope = xform.get_from_section(interaction_name, 'security_scopes', 'security_scope')          
        security_scope = True if security_scope == 'True' else False

        return {'groups': groups,
                'abstract': abstract,
                'status': status,
                'interactionType': interaction_type,
                'contactAddress': contact_address,
                'contactZipPostal': contact_zip_postal,
                'contactPhone': contact_phone,
                'contactLinkedIn': contact_linkedin,
                'contactEmail': contact_email,
                'contactTwitter': contact_twitter,
                'contactName': contact_name,
                'public': security_scope,
                'local_id': xform.make_uid(interaction_name)}

    def _get_status(self, range=4):
        """An internal method to compute a random status to drive UX functionality.

        In the backend the statuses are mapped to integers and defined as.

            Completed: 0
            Scheduled: 1
            Canceled: 2
            Planned: 3
            Unknown: 4
        """
        return random.randrange(0, range)

    def create_objects(self, raw_objects):
        """Create interaction objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all company objects and other helper data.
        """
        final_objects = {
            'interactions': []
        }

        # Temp storage for objects
        tmp_objects = {}

        for object in raw_objects:

            # Capture the right study_name and then fetch the study's ID
            study_xform = studies(rewrite_config_dir=self.RULE_DIR)
            study_name = study_xform.get_name(object[self.RAW_STUDY_NAME])
            study_id = study_xform.make_uid(study_name)

            # Capture the right company_name and then fetch the study's ID
            company_xform = companies(rewrite_rule_dir=self.RULE_DIR)
            company_name = company_xform.get_name(object[self.RAW_COMPANY_NAME])
            company_id = company_xform.make_uid(company_name)

            # Perform basic transformation of company data based upon data in the configuration file
            interaction_xform = interactions(self.RULE_DIR)
            interaction_name = interaction_xform.get_name(object[self.RAW_DATE], study_name, company_name)
            interaction_obj = self._transform_interaction(interaction_name, interaction_xform)
            [interaction_date, interaction_time] = self.util.correct_date(object[self.DATETIME])

            # Set the specific dates for the interaction
            interaction_creation = datetime.now().isoformat()
            year = int(interaction_date[0:4])
            month = int(interaction_date[4:6])
            day = int(interaction_date[6:8])
            hour = int(interaction_time[0:2])
            minute = int(interaction_time[2:3])
            interaction_date_time = datetime(year, month, day, hour=hour, minute=minute).isoformat()

            # TODO the date needs to be fixed potentially with the helper functions included
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
                    "thumbnail": object[self.URL] # TODO this is deprecated
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
