
__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2021-August-30'
__copyright__ = "Copyright 2022 mediumroast.io. All rights reserved."

import os
import re
import spacy

from ..helpers import utilities


class Extract:
    """Perform raw data extract from a folder structure, which is then passed to a human for correction.

    In this form of extraction a folder and one layer deep subfolders is interrogated for key data.  These
    data are then used to generate Mediumroast objects.

    We assume that the topmost folder is the study and any subfolders are substudies. However, if any
    subfolder itself contains a subfolder we won't process it.

    Args:
        dir_name (str): The fully qualified path name (default is '../../sample_data/sample_dir')
        base_url (str): A base URL to use when addressing the files

    Returns:
        list: A list of dicts which can be further processed

    Methods:
        get_data()
            Traverse a simple folder/directory structure infering basics to create objects

    """

    def __init__(self, folder_name='../../sample_data/sample_dir', base_url='file://', model='en_core_web_lg'):
        self.folder = folder_name
        self.base_url = base_url
        self.TRAVERSE_LIMIT = 1  # Define how deep we can go from a directory perspective
        self.idx = 0  # Set the base indexer for substudies

        # Create the nlp obj for NER via spacy
        self.nlp = spacy.load(model)

        # We will use this to determine substudy metadata later
        self.substudies = {}

        # Used for company, study and interaction objects
        self.companies = {}
        self.studies = []
        self.interactions = []

        # Pull in helper utilities so we don't need to repeat simple things
        self.util = utilities()

    # Internal helper methods

    def _decode_folder(self, folder, folder_data, study_name, can_traverse=1):
        # Assume if we're at the topmost folder then that's the study name otherwise it is a substudy name
        # TODO teach this method how to properly traverse 
        self.substudy_name = 'default'
        if can_traverse > 0:
            self.study_name = study_name
        else:
            self.substudy_name = folder.split('/')[-1]
            self.substudies[folder.split('/')[-1]] = {'index': self.idx}
            self.idx += 1

        # Temp storage for the folders
        raw_data = []
        for item in folder_data:
            item_type = 'Unknown'  # Defaults to Unknown, and is set below
            item_type = 'directory' if os.path.isdir(
                folder + '/' + item) else self.util.get_item_type(folder, item)

            if item_type == 'directory' and can_traverse > 0:
                my_items = self._decode_folder(
                    folder + '/' + item, os.listdir(folder + '/' + item), study_name, can_traverse=0)
                raw_data += my_items
                # can_traverse = can_traverse - self.TRAVERSE_LIMIT
            elif item_type != 'directory':
                raw_data.append({
                    'raw_name': item,
                    'interaction_name': item.split('.')[0],
                    'full_path': folder + '/' + item,
                    'type': item_type,
                    # This is a temporary id for unique identification until after ingest
                    'temp_id': self.util.hash_it(item + self.folder + '/' + item + item_type),
                    'substudy': self.substudy_name,
                    'study': self.study_name,
                    'url': self.base_url + folder + '/' + item
                })
            # else:
            #     continue

        return raw_data

    def _convert_list_to_dict(self, my_list):
        """Transform a list into a simple dictionary with an increasing integer being the key.
        """
        idx = 1
        my_dict = {}
        for item in my_list:
            my_dict[idx] = item
            idx+=1
        return my_dict

    def _get_objects(self, study_name):
        # TODO teach _get_objects to traverse directories
        candidate_companies = []
        my_objs = self._decode_folder(self.folder, os.listdir(self.folder), study_name)
        [time, date] = self.util.get_date_time()
        my_text = ""
        # Get dates and raw text from the objects if the type is supported
        for obj in my_objs:
            # Extract essential metadata from PDFs
            if re.match(r'^PDF', obj['type'], re.IGNORECASE):
                [my_meta, my_text] = self.util.get_pdf_meta(
                    obj['full_path'])
                if 'xap' in my_meta:
                    raw_date = my_meta['xap']['CreateDate']
                    [date, time] = raw_date.split('T')
                    obj['date'] = date.replace('-', '')
                    obj['time'] = ''.join(
                        time.split('-')[0].split(':')[0:2])

            # Extract essential metadata from PPTX
            elif re.match(r'^Microsoft PowerPoint', obj['type'], re.IGNORECASE):
                [my_meta, my_text] = self.util.get_pptx_meta(
                    obj['full_path'])
                obj['date'] = my_meta['CreateDate'].strftime("%Y%m%d")
                obj['time'] = my_meta['CreateDate'].strftime("%H%M")

            # Extract essential metadata from DOCX
            elif re.match(r'^Microsoft Word', obj['type'], re.IGNORECASE):
                [my_meta, my_text] = self.util.get_docx_meta(
                    obj['full_path'])
                obj['date'] = my_meta['CreateDate'].strftime("%Y%m%d")
                obj['time'] = my_meta['CreateDate'].strftime("%H%M")

            else:
                obj['date'] = date
                obj['time'] = time

            # Extract the NEs for the doc
            doc = self.nlp(my_text)
            orgs = []
            noises = {}
            idx = 1
            for my_ent in doc.ents:
                my_text = re.sub(r'\n+', ' ', my_ent.text)
                noises[idx] = my_text
                if re.match(r'ORG', my_ent.label_, re.IGNORECASE):
                    orgs.append(my_text)
                idx+=1

            obj['noises'] = noises
            obj['candidate_companies'] = self._convert_list_to_dict(orgs)
            if obj.get('date') == None or obj.get('time') == None:
                obj['date'] = date
                obj['time'] = time
            candidate_companies+=orgs

        # Return the prototype interactions and companies
        return my_objs, self._convert_list_to_dict(candidate_companies)

    # Main extraction method

    def get_data(self, study_name):
        """Read content from a folder to extract key metadata from file names.
        """
        print(study_name)
        return self._get_objects(study_name)
