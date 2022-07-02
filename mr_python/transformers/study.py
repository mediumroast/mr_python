__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-31'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

from os import sep # TODO validate if we need sep from os if not remove this line
import sys, re, datetime
sys.path.append('../')

from mr_python.helpers import utilities
from mr_python.helpers import companies
from .helpers import InteractionHelpers as interactions
import configparser as conf

class Transform:
    """Perform transformation of input data into a proper study object.

    Returns:
        list: A list of dicts which can be pass along to additional utilities and programs

    Methods:
        create_objects()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__ (self, rewrite_config_dir='../src/mediumroast/transformers/', debug=True):
        self.RAW_COMPANY_NAME=7
        self.RAW_STUDY_NAME=6
        self.RAW_DATE=0
        self.REGION=1
        self.COUNTRY=2
        self.STATE_PROVINCE=3
        self.CITY=4
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }
        
        # TODO wrap a try catch loop around the config file read
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['study'])

        # This imports the local utilies from mr_sdk for Python
        self.util=utilities()

        # Set debug to true or false
        self.debug=debug

        # Specify what to skip when processing sections in the conf file
        self.to_skip=r"^description|groups|security_scope|substudies|substudy_definition|substudy_type"

    def _transform_study (self, study_name, extended_rewrite=False):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        
        # Add the items which are either rewritten or not present in the file_name metadata.
        name=self.rules.get('names', study_name) if self.rules.has_option('names', study_name) else study_name
        groups=self.rules.get('groups', study_name) if self.rules.has_option('groups', study_name) else self.rules.get('DEFAULT', 'groups')
        description=self.rules.get('descriptions', study_name) if self.rules.has_option('descriptions', study_name) else self.rules.get('DEFAULT', 'description')
        security_scope=self.rules.get('security_scopes', study_name) if self.rules.has_option('security_scopes', study_name) else self.rules.get('DEFAULT', 'security_scope')
        security_scope=True if security_scope == 'True' else False
        substudies=dict()
        if self.rules.has_option('substudies', study_name):
            for substudy in self.rules.get('substudies', study_name).split('|'):
                substudies[substudy]=dict()
        else: 
            substudies[self.rules.get('DEFAULT', 'substudies')]=dict()
    
        # return the basic structure of the study
        return {'name': name, 
                'groups': groups,
                'public': security_scope, 
                'description': description,
                'substudies': substudies}


    # INTERNAL METHODS AND HELPER FUNCTIONS

    def _reformat_name(self, study_name, separator='_'):
        """Internal method to reformat the study name by replacing spaces with the separator."""
        return study_name.replace(' ', separator)


    #############################################################################################
    # All methods to create a study's document which include:
    #   - Introduction
    #   - Opportunity
    #   - Actions
    ############################################################################################# 
    # Transform either default or study specific document elements into the proper data structure
    def _document_helper(self, section, seperator='_'):
        intro='Introduction'
        opp='Opportunity'
        acts='Action'
        document={
            intro: '',
            opp: {},
            acts: {}
        }
        introduction=re.compile('^Introduction', re.IGNORECASE)
        opportunities=re.compile('^Opportunity_', re.IGNORECASE)
        actions=re.compile('^Action_', re.IGNORECASE)
        for idx in list(self.rules[section]):
            if introduction.match(idx): 
                document[intro]=self.rules[section][idx]
            elif opportunities.match(idx):
                item_type=idx.split(seperator)[1]
                if item_type == 'Text': document['Opportunity']['text']=self.rules[section][idx]
                else: document['Opportunity'][item_type]=self.rules[section][idx]
            elif actions.match(idx):
                item_type=idx.split(seperator)[1]
                if item_type == 'Text': document['Action']['text']=self.rules[section][idx]
                else: document['Action'][item_type]=self.rules[section][idx]
        return document

    def _get_document (self, study_name, default='DEFAULT_PRFAQ'):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        section=self._reformat_name(study_name) + '_PRFAQ'
        document=self._document_helper(section) if self.rules.has_section(section) else self._document_helper(default)
        return document

   
    #############################################################################################
    # All methods to create a substudy attributes, which include:
    #   - Interactions
    #   - Questions
    #   - Themes
    #   - Theme Quotes
    #   - Theme Frequencies
    #############################################################################################
    # Pull in the interactions to the substudy
    def _get_interactions(self, interactions, substudy, interaction_xform):
        """Internal method to create the iterations structure"""
        final_interactions={}
        for interaction in interactions:
            substudy_id, company_itr_id=interaction_xform.get_substudy_id(interaction)
            if substudy_id == substudy:
                final_interactions[interaction]={
                        "GUID": interactions[interaction],
                        "abstractState": False # set the default to False
                }
            else: continue
        return final_interactions
    
    # Transform either default or study specific keytheme quotes into the proper data structure
    def _quotes_helper(self, section, separator='<->', sub_separator='|'):
        """Helper method for _get_keytheme_quotes to obtain, parse, format and return the quotes"""
        quotes={}
        many_quotes=re.compile(separator) # For the case when there are more than 1 quote per theme
        to_skip=re.compile(self.to_skip, re.IGNORECASE)
        for idx in list(self.rules[section]):
            if to_skip.match(idx): continue
            if many_quotes.search(self.rules[section][idx]): # More than 1 quote
                quotes[idx]={}
                for set in self.rules[section][idx].split(separator):
                    (quote, name)=set.split(sub_separator)
                    quotes[idx][name]=quote
            else: # Only 1 quote
                (quote, name)=self.rules[section][idx].split(sub_separator)
                quotes[idx]={name: quote}
        return quotes

    def _get_theme_quotes (self, study_name, substudy):
        """Internal method to obtain either the default set of keytheme quotes or the study specific set of quotes."""
        section=self._reformat_name(study_name) + '_Substudy_' + substudy + '_Theme_Quotes'
        quotes=self._quotes_helper(section) if self.rules.has_section(section) else dict()
        return quotes

    # Transform either default or study specific keytheme frequencies into the proper data structure
    def _frequencies_helper(self, section, separator=',', sub_separator='|'):
        """Helper method for _get_keytheme_frequencies to obtain, parse, format and return the frequencies."""
        frequencies={}
        to_skip=re.compile(self.to_skip, re.IGNORECASE)
        for idx in list(self.rules[section]):
            if to_skip.match(idx): continue
            for set in self.rules[section][idx].split(separator):
                (name, frequency)=set.split(sub_separator)
                frequencies[idx]={name: frequency}
        return frequencies

    def _get_theme_frequencies(self, study_name, substudy):
        """Internal method to obtain either the default set of keytheme frequencies or the study specific set of frequencies."""
        section=self._reformat_name(study_name) + '_Substudy_' + substudy + '_Theme_Frequencies'
        frequencies=self._frequencies_helper(section) if self.rules.has_section(section) else dict()
        return frequencies

    # Transform either default or study specific keythemes into the proper data structure
    def _themes_helper(self, section, separator='|'):
        """Helper method for _get_keythemes to obtain, parse, format and return the themes."""
        themes=dict()
        to_skip=re.compile(self.to_skip, re.IGNORECASE)
        for idx in list(self.rules[section]):
            if to_skip.match(idx): continue
            theme=self.rules[section][idx].split(separator)
            themes[idx]={
                "name": theme[0],
                "description": theme[1],
                "frequency": theme[2]
            }
        return themes
    
    def _get_themes(self, study_name, substudy):
        """Internal method to obtain either the default set of keythemes or the study specific set of keythemes."""
        section=self._reformat_name(study_name) + '_Substudy_' + substudy + '_Theme_Definitions'
        # If there is a themes section for this substudy define it otherwise return an empty dict
        themes=self._themes_helper(section) if self.rules.has_section(section) else dict()
        return themes
    
    # Transform either default or study specific questions into the proper data structure
    def _questions_helper(self, section, separator='|'):
        """Helper method for _get_questions to obtain, parse, format and return a question."""
        questions=dict()
        to_skip=re.compile(self.to_skip, re.IGNORECASE)
        for idx in list(self.rules[section]):
            if to_skip.match(idx): continue
            question=self.rules[section][idx].split(separator)
            state=True if question[1] == 'True' else False
            questions[idx]={
                "question": question[0],
                "notes": question[2],
                "included": state
            }
        return questions

    def _get_questions(self, study_name, substudy):
        """Internal method to obtain either the default set of questions or the study specific set of questions."""
        section=self._reformat_name(study_name) + '_Substudy_' + substudy + '_Questions'
        questions=self._questions_helper(section) if self.rules.has_section(section) else dict()
        return questions

    def _noises_helper(self, section):
        """Helper method for _get_noises to obtain, parse, format and return the noises."""
        noises=dict()
        to_skip=re.compile(self.to_skip, re.IGNORECASE)
        for idx in list(self.rules[section]):
            if to_skip.match(idx): continue
            noise=self.rules[section][idx]
            noises[idx]=noise
        return noises
    
    def _get_noises(self, study_name, substudy):
        """Internal method to obtain the set of study noises if they exist."""
        section=self._reformat_name(study_name) + '_Substudy_' + substudy + '_Noises'
        noises=self._noises_helper(section) if self.rules.has_section(section) else dict()
        return noises

    def _get_substudy_type(self, study_name, substudy):
        section=self._reformat_name(study_name) + '_Substudy_Types'
        substudy_type=self.rules.get(section, substudy) if self.rules.has_option(section, substudy) else self.rules.get('DEFAULT', 'substudy_type')
        return substudy_type

    def _make_substudies(self, study, interaction_xform):
        theme_state=False # Define the default state of a substudy's theme; NOTE: should assign only after we detect if there are more than system assigned default themes
        final_substudies=dict() # Where we will store the final structure to be returned
        config_pre=self._reformat_name(study['studyName']) + '_Substudy_'

        # Process each substudy
        for substudy in study['substudies'].keys():
            definition=self.rules.get(config_pre + 'Definitions', substudy) if self.rules.has_section(config_pre + 'Definitions') else self.rules.get('DEFAULT', 'substudy_definition')
            name, description=definition.split('|')
            guid=self.util.hash_it(name + description) # For now set the GUID to be the combo of name and description, may be overidden by the DB in the future.
            final_substudies[substudy]={
                'type': self._get_substudy_type(study['studyName'], substudy),
                'totalInteractions': 0, # Set this sum to 0
                'totalQuestions': 0, # Set this sum to 0
                'totalThemes': 0, # Set this sum to 0
                'noiseText': self._get_noises(study['studyName'], substudy),
                'name': name,
                'description': description,
                'GUID': guid,
                'interactions': self._get_interactions(study['linkedInteractions'], substudy, interaction_xform), # This needs to be reworked to get the substudy interactions
                'questions': self._get_questions(study['studyName'], substudy),
                'keyThemes': self._get_themes(study['studyName'], substudy),
                'keyThemeQuotes': self._get_theme_quotes(study['studyName'], substudy),
            }
            final_substudies[substudy]['totalInteractions']=self.util.total_item(final_substudies[substudy]['interactions'])
            final_substudies[substudy]['totalQuestions']=self.util.total_item(final_substudies[substudy]['questions'])
            final_substudies[substudy]['totalThemes']=self.util.total_item(final_substudies[substudy]['keyThemes'])
            if final_substudies[substudy]['totalThemes'] > 0: theme_state=True
            final_substudies[substudy]['themeState']=theme_state
        return final_substudies

    def _get_date (self):
        my_date = datetime.date.today()
        return my_date.year + my_date.month + my_date.day
    
    def _get_time (self):
        my_date = datetime.time
        return my_date.hour + my_date.minute
        
        # Process each substudy
        for substudy in study['substudies'].keys():
            definition=self.rules.get(config_pre + 'Definitions', substudy) if self.rules.has_section(config_pre + 'Definitions') else self.rules.get('DEFAULT', 'substudy_definition')
            name, description=definition.split('|')
            guid=self.util.hash_it(name + description) # For now set the GUID to be the combo of name and description, may be overidden by the DB in the future.
            final_substudies[substudy]={
                'date': self._get_date(),
                'time': self._get_time(),
                'type': self._get_substudy_type(study['studyName'], substudy),
                'totalInteractions': 0, # Set this sum to 0
                'totalQuestions': 0, # Set this sum to 0
                'totalThemes': 0, # Set this sum to 0
                'noiseText': self._get_noises(study['studyName'], substudy),
                'name': name,
                'description': description,
                'GUID': guid,
                'interactions': self._get_interactions(study['linkedInteractions'], substudy, interaction_xform), # This needs to be reworked to get the substudy interactions
                'questions': self._get_questions(study['studyName'], substudy),
                'keyThemes': self._get_themes(study['studyName'], substudy),
                'keyThemeQuotes': self._get_theme_quotes(study['studyName'], substudy),
            }
            final_substudies[substudy]['totalInteractions']=self.util.total_item(final_substudies[substudy]['interactions'])
            final_substudies[substudy]['totalQuestions']=self.util.total_item(final_substudies[substudy]['questions'])
            final_substudies[substudy]['totalThemes']=self.util.total_item(final_substudies[substudy]['keyThemes'])
            if final_substudies[substudy]['totalThemes'] > 0: theme_state=True
            final_substudies[substudy]['themeState']=theme_state
        return final_substudies


    # EXTERNAL METHODS AND HELPER FUNCTIONS
    def create_objects (self, raw_objects, file_output=True):
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
        interaction_xform=interactions(self.RULES['dir'])  
        company_xform=companies(rewrite_config_dir=self.RULES['dir'])

        # Temp storage for objects
        tmp_objects={}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            study_obj=self._transform_study(object[self.RAW_STUDY_NAME])

            # Capture the right company_name and then fetch the study's ID
            company_name = company_xform.get_name(object[self.RAW_COMPANY_NAME])
            company_id = company_xform.make_id(company_name)
            
            # Capture the right study_name and then fetch the study's ID
            interaction_name=interaction_xform.get_name(object[self.RAW_DATE], study_obj['name'], company_name)
            interaction_id=interaction_xform.make_uid(interaction_name)

            if tmp_objects.get (object[self.RAW_STUDY_NAME]) == None:
                tmp_objects[object[self.RAW_STUDY_NAME]] = {
                    "studyName": study_obj['name'],
                    "description": study_obj['description'],
                    "linkedCompanies": {company_name: company_id},
                    "totalCompanies": 0,
                    "linkedInteractions": {interaction_name: interaction_id},
                    "totalInteractions": 0,
                    "substudies": study_obj['substudies'],
                    "document": self._get_document(study_obj['name']),
                    "public": study_obj['public'],
                    "groups": study_obj['groups']
                    ### TODO Notes could be transformed into the opportunity or similar
                }
            else:
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedCompanies"][company_name]=company_id
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedInteractions"][interaction_name]=interaction_id

        for study in tmp_objects.keys ():
            if file_output:
                # Generally the model to create a GUID is to hash the name and the description for all objects.
                # We will only use this option when we're outputing to a file.
                guid=self.util.hash_it(study + tmp_objects[study]['description'])
                tmp_objects[study]['GUID']=guid
                tmp_objects[study]['id']=guid
            
            tmp_objects[study]['totalInteractions']=self.util.total_item(tmp_objects[study]['linkedInteractions'])
            tmp_objects[study]['totalCompanies'] = self.util.total_item(tmp_objects[study]['linkedCompanies'])
            tmp_objects[study]['substudies']=self._make_substudies(tmp_objects[study], interaction_xform,)
            final_objects['studies'].append(tmp_objects[study])

        return final_objects

    