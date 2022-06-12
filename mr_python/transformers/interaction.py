__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-September-12'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

import sys, random
sys.path.append('../')

from mr_python.helpers import utilities
from mr_python.helpers import companies
from mr_python.helpers import interactions
from mr_python.helpers import studies
import configparser as conf

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

    def __init__ (self, rewrite_config_dir='../src/mediumroast/transformers/', debug=False):
        # TODO consume the additional defaults for URL, etc.
        self.RAW_COMPANY_NAME=7
        self.RAW_STUDY_NAME=6
        self.RAW_DATE=0
        self.REGION=1
        self.COUNTRY=2
        self.STATE_PROVINCE=3
        self.CITY=4
        self.URL=9
        self.THUMBNAIL=10
        self.DATETIME=0
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }
        
        # TODO wrap a try catch loop around the config file read
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['interaction'])

        # This imports the local utilies from mr_sdk for Python
        self.util=utilities()

        # Set debug to true or false
        self.debug=debug

        # TODO Update for this object type and put into the various helper methods.  This is wrong as of now
        # Specify what to skip when processing sections in the conf file
        self.to_skip=r"^description|groups|security_scope|substudies|substudy_definition|substudy_type"

    # TODO rewrite this to follow the load_studies utility

    def _transform_interaction (self, interaction_name):
        """Internal method to rewrite or augment key aspects of an interaction object as per definitions in the configuration file."""
        
        # Add the items which are either rewritten or not present in the file_name metadata.
        groups=self.rules.get('groups', interaction_name) if self.rules.has_option('groups', interaction_name) else self.rules.get('DEFAULT', 'groups')
        abstract=self.rules.get('abstracts', interaction_name) if self.rules.has_option('abstracts', interaction_name) else self.rules.get('DEFAULT', 'abstract')
        status=self.rules.get('statuses', interaction_name) if self.rules.has_option('statuses', interaction_name) else self.rules.get('DEFAULT', 'status')
        interaction_type=self.rules.get('types', interaction_name) if self.rules.has_option('types', interaction_name) else self.rules.get('DEFAULT', 'type')
        contact_address=self.rules.get('contact_addresses', interaction_name) if self.rules.has_option('contact_addresses', interaction_name) else self.rules.get('DEFAULT', 'contact_address')
        contact_zipPostal=self.rules.get('contact_zipPostals', interaction_name) if self.rules.has_option('contact_zipPostals', interaction_name) else self.rules.get('DEFAULT', 'contact_zipPostal')
        contact_phone=self.rules.get('contact_phones', interaction_name) if self.rules.has_option('contact_phones', interaction_name) else self.rules.get('DEFAULT', 'contact_phone')
        contact_linkedin=self.rules.get('contact_linkedins', interaction_name) if self.rules.has_option('contact_linkedins', interaction_name) else self.rules.get('DEFAULT', 'contact_linkedin')
        contact_email=self.rules.get('contact_emails', interaction_name) if self.rules.has_option('contact_emails', interaction_name) else self.rules.get('DEFAULT', 'contact_email')
        contact_twitter=self.rules.get('contact_twitters', interaction_name) if self.rules.has_option('contact_twitters', interaction_name) else self.rules.get('DEFAULT', 'contact_twitter')
        contact_name=self.rules.get('contact_names', interaction_name) if self.rules.has_option('contact_names', interaction_name) else self.rules.get('DEFAULT', 'contact_name')
        security_scope=self.rules.get('security_scopes', interaction_name) if self.rules.has_option('security_scopes', interaction_name) else self.rules.get('DEFAULT', 'security_scope')
        security_scope=True if security_scope == 'True' else False

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
        idx=random.randrange(0, range)
        statuses=['Completed', 'Scheduled', 'Canceled', 'Planned', 'Unknown']
        return statuses[idx]

 
    def create_objects (self, raw_objects, file_output=True):
        """Create study objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all company objects and the total number of company objects processed
        """
        final_objects={
            'totalInteractions': 0,
            'interactions': []
        }  

        # Temp storage for objects
        tmp_objects={}

        for object in raw_objects:

            # Capture the right study_name and then fetch the study's ID
            study_xform=studies(rewrite_config_dir=self.RULES['dir'])
            study_name=study_xform.get_name (object[self.RAW_STUDY_NAME]) 
            study_id=study_xform.make_id (study_name) 

            # Capture the right company_name and then fetch the study's ID
            company_xform=companies(rewrite_config_dir=self.RULES['dir'])
            company_name=company_xform.get_name (object[self.RAW_COMPANY_NAME])
            company_id=company_xform.make_id (company_name) 
            
            # Perform basic transformation of company data based upon data in the configuration file
            interaction_xform=interactions(rewrite_config_dir=self.RULES['dir'])
            interaction_name=interaction_xform.get_name(object[self.RAW_DATE], study_name, company_name)
            interaction_obj=self._transform_interaction(interaction_name)
            interaction_date, interaction_time=self.util.correct_date(object[self.DATETIME])

                        
            # TODO the date needs to be fixed potentially with the helper functions included
            # TODO this is only partially implemented and needs to be looked at again
            if tmp_objects.get (interaction_name) == None:
                long_lat = self.util.locate (object[self.CITY] + ',' + object[self.STATE_PROVINCE] + ',' + object[self.COUNTRY])
                tmp_objects[interaction_name] = {
                    "interactionName": interaction_name,
                    "time": interaction_time,
                    "date": interaction_date,
                    "state": "unsummarized",
                    "simpleDesc": interaction_xform.get_description(company_name, study_name),
                    "contactAddress": interaction_obj['contactAddress'],
                    "contactZipPostal": interaction_obj['contactZipPostal'],
                    "contactPhone": interaction_obj['contactPhone'],
                    "contactLinkedIn": interaction_obj['contactLinkedIn'],
                    "contactEmail": interaction_obj['contactEmail'],
                    "contactTwitter": interaction_obj['contactTwitter'],
                    "contactName": interaction_obj['contactName'],
                    "public": interaction_obj['public'],
                    "abstract": interaction_obj['abstract'],
                    "interactionType": interaction_obj['interactionType'],
                    "status": self._get_status(),
                    "linkedStudies": {study_name: study_id},
                    "linkedCompanies": {company_name: company_id},
                    "longitude": long_lat[0],
                    "latitude": long_lat[1],
                    "url": object[self.URL],
                    "thumbnail": object[self.THUMBNAIL],
                    "notes": self.util.make_note(obj_type='Interaction Object: [' + interaction_name + ']')
                }
            else:
                tmp_objects[interaction_name]["linkedStudies"][study_name]=study_id
                tmp_objects[interaction_name]["linkedCompanies"][company_name]=company_id


        # TODO Look at the study.py module for the right approach here
        for interaction in tmp_objects.keys ():
            if file_output:
                # Generally the model to create a GUID is to hash the name and the description for all objects.
                # We will only use this option when we're outputing to a file.
                guid=self.util.hash_it(interaction + tmp_objects[interaction]['simpleDesc'])
                tmp_objects[interaction]['GUID']=guid
                tmp_objects[interaction]['id']=guid
            tmp_objects[interaction]['totalStudies']=self.util.total_item(tmp_objects[interaction]['linkedStudies'])
            tmp_objects[interaction]['totalCompanies']=self.util.total_item(tmp_objects[interaction]['linkedCompanies'])
            final_objects['interactions'].append (tmp_objects[interaction])

        final_objects['totalInteractions'] = self.util.total_item(final_objects['interactions'])

        return final_objects

    