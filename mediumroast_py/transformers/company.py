__version__ = '2.0'
__author__ = "Michael Hay"
__date__ = '2022-June-25'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import json

# Perform local imports
from .helpers import InteractionHelpers as interactions
from .helpers import CompanyHelpers as companies
from .helpers import StudyHelpers as studies
from ..helpers import utilities

class Transform:
    """Perform the core transformation of input data into a proper company object.

    Using the transformation rules written into the rules files specified in 'rewrite_rule_dir'
    create more complete company objects which can then be ingested into the backend. This
    kind of transformation can be used from any input like files, file systems and S3 compatible
    object stores where the source data can be massaged into a the following array of arrays.

    '
        [
            [RAW_DATE, REGION, COUNTRY, STATE_PROVINCE, CITY, INDUSTRY, RAW_STUDY_NAME, RAW_COMPANY_NAME, INTERACTION_TYPE, URL],
            ...
            [RAW_DATE, REGION, COUNTRY, STATE_PROVINCE, CITY, INDUSTRY, RAW_STUDY_NAME, RAW_COMPANY_NAME, INTERACTION_TYPE, URL]
        ]
    '

    This input is passed to `create_objects` which in turn generates a dict that contains a list of the company objects
    and associated metadata.  (Note, that at this time the metadata is still under construction and the documentation will
    be updated when ready.)  These company objects can then be iterated over and ingested into the backend.  
    Finally, if the 'debug' argument is set to True then this transformation class will print out every object prior to returning -- the default value of 'debug' is false.  This output is extremely useful if you're making modifications
    to the transformation and need to debug the results with an external tool like Postman.
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

    def _transform_company(self, company_name, xform):
        """Internal method to rewrite or augment key aspects of a company object as per definitions in the configuration file.""" 

        # Add the items which are either rewritten or not present in the file_name metadata.
        name = xform.get_from_section(company_name, 'names', 'name')
        industry = xform.get_from_section(company_name, 'industries', 'industry')
        role = xform.get_from_section(company_name, 'roles', 'role')
        description = xform.get_from_section(company_name, 'descriptions', 'description')
        url = xform.get_from_section(company_name, 'urls', 'url')
        cik = xform.get_from_section(company_name, 'ciks', 'cik')
        stockSymbol = xform.get_from_section(company_name, 'stockSymbols', 'stockSymbol')
        recent10kURL = xform.get_from_section(company_name, 'recent10kURLs', 'recent10kURL')
        recent10qURL = xform.get_from_section(company_name, 'recent10qURLs', 'recent10qURL')
        phone = xform.get_from_section(company_name, 'phones', 'phone')
        zipPostal = xform.get_from_section(company_name, 'zipPostals', 'zipPostal')
        stateProvince = xform.get_from_section(company_name, 'stateProvinces', 'stateProvince')
        city = xform.get_from_section(company_name, 'cities', 'city')
        country = xform.get_from_section(company_name, 'countries', 'country')
        region = xform.get_from_section(company_name, 'regions', 'region')
        latitude = xform.get_from_section(company_name, 'latitudes', 'latitude')
        longitude = xform.get_from_section(company_name, 'longitudes', 'longitude')
        streetAddress = xform.get_from_section(company_name, 'streetAddresses', 'streetAddress')
        logo = xform.get_from_section(company_name, 'logos', 'logo')
        logo_url = logo

        return {'name': company_name,
                'role': role,
                'industry': industry,
                'description': description,
                'url': url,
                'logo_url': logo_url,
                'streetAddress': streetAddress,
                'city': city,
                'stateProvince': stateProvince,
                'country': country,
                'region': region,
                'phone': phone,
                'cik': cik,
                'stockSymbol': stockSymbol,
                'recent10kURL': recent10kURL,
                'recent10qURL': recent10qURL,
                'latitude': latitude,
                'longitude': longitude,  
                'zipPostal': zipPostal}


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
        interaction_xform = interactions(self.RULE_DIR)
        study_xform = studies(self.RULE_DIR)
        company_xform = companies(self.RULE_DIR)

        # Temp storage for objects
        tmp_objects = {}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            company_obj = self._transform_company(object[self.RAW_COMPANY_NAME], company_xform)

            # Capture the right study_name and then fetch the study's ID
            study_name = study_xform.get_name(object[self.RAW_STUDY_NAME])
            study_id = study_xform.make_uid(study_name)

            # Capture the right study_name and then fetch the study's ID
            interaction_name = interaction_xform.get_name(
                object[self.RAW_DATE], study_name, company_obj['name'])
            interaction_id = interaction_xform.make_uid(interaction_name)

            if tmp_objects.get(object[self.RAW_COMPANY_NAME]) == None:
                # Set the lat long pair
                long_lat = self.util.locate(
                    object[self.CITY] + ',' 
                    + object[self.STATE_PROVINCE] + ',' 
                    + object[self.COUNTRY]) if company_obj['latitude'] == 'Unknown' or company_obj['longitude'] == 'Unknown' else [company_obj['longitude'], company_obj['latitude']]

                tmp_objects[object[self.RAW_COMPANY_NAME]] = {
                    "name": company_obj['name'],
                    "industry": company_obj['industry'],
                    "role": company_obj['role'],
                    "url": company_obj['url'],
                    "logo_url": company_obj['logo_url'],
                    "icon": company_obj['logo_url'], # TODO this is deprecated
                    "street_address": company_obj['streetAddress'],
                    "city": object[self.CITY] if company_obj['city'] == 'Unknown' else company_obj['city'],
                    "state_province": object[self.STATE_PROVINCE] if company_obj['stateProvince'] == 'Unknown' else company_obj['stateProvince'],
                    "country": object[self.COUNTRY] if company_obj['country'] == 'Unknown' else company_obj['country'],
                    "region": object[self.REGION] if company_obj['region'] == 'Unknown' else company_obj['region'],
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
                    "document": company_xform.get_document(company_obj['name']),
                    "topics": {
                        "some words": 10.0,
                        "more words": 1.1
                    },
                    "comparison": {
                        "Company 1": 1.0,
                        "Company 2": 10.1
                    }
                }
            else:
                tmp_objects[object[self.RAW_COMPANY_NAME]]["linked_studies"][study_name] = study_id
                tmp_objects[object[self.RAW_COMPANY_NAME]]["linked_interactions"][interaction_name] = interaction_id

        for company in tmp_objects.keys():
            # In case we're debugging print out each object
            if self.debug: print(json.dumps(tmp_objects[company]))

            final_objects['companies'].append(tmp_objects[company])

        return final_objects
