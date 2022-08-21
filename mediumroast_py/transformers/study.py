__version__ = '2.0'
__author__  = "Michael Hay"
__date__    = '2022-July-03'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import json

# Perform local imports
from .helpers import InteractionHelpers as interactions
from .helpers import CompanyHelpers as companies
from .helpers import StudyHelpers as studies
from ..helpers import utilities

class Transform:
    """Perform the core transformation of input data into a proper study object.

    Using the transformation rules written into the rules files specified in 'rewrite_rule_dir'
    create more complete study objects which can then be ingested into the backend. This
    kind of transformation can be used from any input like files, file systems and S3 compatible
    object stores where the source data can be massaged into a the following array of arrays.

    '
        [
            [RAW_DATE, REGION, COUNTRY, STATE_PROVINCE, CITY, INDUSTRY, RAW_STUDY_NAME, RAW_COMPANY_NAME, INTERACTION_TYPE, URL],
            ...
            [RAW_DATE, REGION, COUNTRY, STATE_PROVINCE, CITY, INDUSTRY, RAW_STUDY_NAME, RAW_COMPANY_NAME, INTERACTION_TYPE, URL]
        ]
    '

    This input is passed to `create_objects` which in turn generates a dict that contains a list of the study objects
    and associated metadata.  (Note, that at this time the metadata is still under construction and the documentation will
    be updated when ready.)  These study objects can then be iterated over and ingested into the backend.  
    Finally, if the 'debug' argument is set to True then this transformation class will print out every object prior to returning -- the default value of 'debug' is false.  This output is extremely useful if you're making modifications
    to the transformation and need to debug the results with an external tool like Postman.

    Future work:

    There is a requirement to implement 'linked_companies" and 'linked_interactions' attributes for
    the study/substudy objects.  This depends on the backend implementation and may be more complex that the initial 
    implementation with the 'json_server'.  There are some breadcrumbs and notes in the comments for this linking process
    within the transformation code.

    Additionally, the substudies implementation needs to be worked on and synced with the backend.
    """

    def __init__ (self, rewrite_rule_dir, debug=True):
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

    def _transform_study (self, study_name, xform):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        
        # Add the items which are either rewritten or not present in the file_name metadata.
        name = xform.get_name(study_name)
        groups = xform.get_from_section(study_name, 'groups', 'groups')
        description = xform.get_from_section(study_name, 'descriptions', 'description')
        security_scope = xform.get_from_section(study_name, 'security_scopes', 'security_scope')
        security_scope = True if security_scope == 'True' else False

        # TODO verify how we will work substudies
        # substudies=dict()
        # if self.rules.has_option('substudies', study_name):
        #     for substudy in self.rules.get('substudies', study_name).split('|'):
        #         substudies[substudy]=dict()
        # else: 
        #     substudies[self.rules.get('DEFAULT', 'substudies')]=dict()
    
        # return the basic structure of the study
        return {'name': name, 
                'groups': groups,
                'public': security_scope, 
                'description': description}
                # 'substudies': substudies}
    

    # EXTERNAL METHODS AND HELPER FUNCTIONS
    def create_objects (self, raw_objects):
        """Create study objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all study objects and the total number of study objects processed
        """
        final_objects={
            'studies': []
        }

        # Construct objects
        interaction_xform = interactions(self.RULE_DIR)  
        company_xform = companies(self.RULE_DIR)
        study_xform = studies(self.RULE_DIR)

        # Temp storage for objects
        tmp_objects={}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            study_obj=self._transform_study(object[self.RAW_STUDY_NAME], study_xform)

            # Capture the right company_name and then fetch the study's ID
            company_name = company_xform.get_name(object[self.RAW_COMPANY_NAME])
            company_id = company_xform.make_uid(company_name)

            # Capture the right study_name and then fetch the study's ID
            interaction_name = interaction_xform.get_name(
                object[self.RAW_DATE], study_obj['name'], company_name)
            interaction_id = interaction_xform.make_uid(interaction_name)
            

            if tmp_objects.get (object[self.RAW_STUDY_NAME]) == None:
                tmp_objects[object[self.RAW_STUDY_NAME]] = {
                    "name": study_obj['name'], # TODO This will change to name in a future backend version
                    "description": study_obj['description'],
                    "linked_companies": {company_name: company_id}, # TODO discussion how we should do linked_companies
                    "linked_interactions": {interaction_name: interaction_id}, # TODO discussion how we should do linked_companies
                    # "substudies": study_obj['substudies'], # TODO discuss the substudies implementation and correct
                    "document": study_xform.get_document(study_obj['name']),
                    "public": study_obj['public'],
                    "groups": study_obj['groups']
                    ### TODO Notes could be transformed into the opportunity or similar
                }
            else:
                tmp_objects[object[self.RAW_STUDY_NAME]]["linked_companies"][company_name] = company_id
                tmp_objects[object[self.RAW_STUDY_NAME]]["linked_interactions"][interaction_name] = interaction_id

        for study in tmp_objects.keys():
            # In case we're debugging print out each object
            if self.debug: print(json.dumps(tmp_objects[study]))
            
            # TODO discuss the substudies implementation and correct
            # tmp_objects[study]['substudies']=self._make_substudies(tmp_objects[study], interaction_xform,)
            final_objects['studies'].append(tmp_objects[study])

        return final_objects

    