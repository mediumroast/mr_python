__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import configparser as conf
import re

# Perform local imports
from ..helpers import utilities as util

class BaseHelpers:
    def __init__(self, rewrite_rule_dir, obj_type):

        # Match the object type to the rule file and pull in the rule file
        _rule_type = {
            'company': 'company.ini',
            'interaction': 'interaction.ini',
            'study': 'study.ini',
        }
        self.rule_dir = rewrite_rule_dir
        self.rule_file = self.rule_dir + '/' + _rule_type[obj_type]
        self.rewrite_rules = conf.ConfigParser()
        self.rewrite_rules.read(self.rule_file)

        # Pull in the utilities
        self.util = util()

    def make_uid(self, name, extra_text=None):
        """Create a locally unique identifier for an object, and if extra_text is included add it in.

        This text is needed for ingestion when we are going to keep ourselves straight for linking
        various objects. Since the backend keeps unique identifiers per object and they aren't known
        before we ingest we need a way, other than the name, to clearly identify the object.  This local
        and unique identifier should not be ingested into the backend as this will cause an error.  

        Additionally, since it is possible to have duplicated objects it is highly encouraged to 
        add something like a string of the ingest time, which is the initial creation time, along 
        with the name of the object when creating a locally unique identifier.  For an example of
        this in action check out examples/s3_ingest.py.

        Finally, it is recommended that the identifier be created with the results from the
        'get_name' method.
        """

        # Define the id_text with or without the extra_text, default is without
        id_text = name + extra_text if extra_text else name

        return self.util.hash_it(id_text)

    def get_name(self, raw_name):
        """Should there be a rewritten name in the rule file capture it and return it.

        In a rewrite rules file there is a [names] section with 'raw_name=new name' set.
        This method will take in 'raw_name' and return 'new name'.  If there is no
        match for 'raw_name' in the section then 'raw_name' will be returned. 
        """

        # Set to the rewritten name if it exists otherwise set to the original raw_name
        obj_name = self.rewrite_rules['names'][raw_name] if self.rewrite_rules.has_option('names', raw_name) else raw_name

        return obj_name

    def get_description(self, name):
        """Using the 'name' of the object return a unique description, if it exists, otherwise return the default.

        In a rewrite rules file there is a [descriptions] section with 'name=description' set.
        This method will take in 'name' and return 'description'.  If there is no
        match for 'name' in the section then the description from the [DEFAULT] section will be returned. 
        """

        # Return the rewritten description if it exists otherwise return the DEFAULT description
        return self.get_from_section(name, 'descriptions', 'description')

    def get_groups(self, raw_name):
        """Using the 'raw_name' of the object return the associated groups, if it exists, otherwise return the default.

        In a rewrite rules file there is a [groups] section with 'raw_name=groups' set.
        This method will take in 'raw_name' and return 'groups'.  If there is no
        match for 'raw_name' in the section then the groups from the [DEFAULT] section will be returned. 
        """

        # Return the rewritten description if it exists otherwise return the DEFAULT description
        return self.get_from_section(raw_name, 'groups', 'groups')

    def get_from_section(self, name, section, default_name, default_section='DEFAULT'):
        """A generic method to return either 'name' from 'section' or 'default_name' from 'DEFAULT'

        This generic method enables subclasses to more easily create specific methods for getting
        rewrite rules.  As needed it can also be directly used.
        """

        obj_value = self.rewrite_rules[section][name] if self.rewrite_rules.has_option(section, name) else self.rewrite_rules[default_section][default_name]

        return obj_value

class InteractionHelpers(BaseHelpers):
    def __init__(self, rewrite_rule_dir, obj_type='interaction'):
        super().__init__(rewrite_rule_dir, obj_type)

        # NOTE This is the template description which also shows up in the 'interaction.ini'
        #       rule file.  You will need to update in both places if you plan to customize.
        self.desc_template = 'Learn from COMPANY, either in person or digitally, key points and inputs related to the study STUDYNAME.'

    def get_name(self, date, study_name, company_name):
        """Construct an object name using key system metadata including study and company names, plus a date.

        This method overrides the default method from the parent class because when S3 ingesting occurs there
        isn't a direct name for the interaction.  So, it becomes necessary to have the transformation logic
        automatically construct it.  The returned string is 'YYYYMMDDHHMM-study_name-company_name'.  Other
        ingestion implementations might be able to detect the interaction name in other ways therefore this
        logic may not be required.

        Args:
            study_name (str): The study the interaction is associated to.
            company_name (str): The company the interaction is associated to.
            date (str): A raw date for the interaction, this needs to be the same date fed to the interaction transform

        Returns:
            string: The generated name of the interaction which is the synthesis of the date string and study name
        """

        # Return the system generated name from key system metadata
        return str(date) + '-' + str(study_name) + '-' + str(company_name)

    def get_description(self, study_name, company_name, name='NULL'):
        """Create a description for the interaction.

        Using a default in the rule file merge in company and study names to generate a description for the interaction. Currently the default description template in the rule file is:

        'Learn from COMPANY, either in person or digitally, key points and inputs related to the study STUDYNAME' 

        The implementation then replaces 'COMPANY' and 'STUDYNAME' with the inputs to this method.
        While it is possible to change the template it is highly discouraged.  If you were to do it
        you'd need to update the used 'interaction.ini' file, and this module accordingly.  Comments
        in the code point to where potential changes are needed. A better approach would be to make
        use of a specific description for the relevant interactions that need to be updated.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            study_name (str): The study name which aligns to the name within the configuration file.
            name (str): An optional name to lookup a description for, defaults to None

        Returns:
            my_description (str): A generated textual description generated from the company and study names.
        """

        my_description = super().get_description(name)
        if my_description == self.desc_template:
            # NOTE these are the replacement rules to update the interaction description.
            #       If you choose to create your own implementation these two replacements
            #       will need to be updated to match your approach.
            my_description = my_description.replace("COMPANY", str(company_name))
            return my_description.replace("STUDYNAME", str(study_name))
        else:
            return my_description

    def get_substudy_id(self, interaction_name):
        """Lookup substudy ids and return them.

        If there are rewrite rules available for the interaction name mapping it to a substudy Id for
        the associated study return it else return the default substudy Id.  Substudy Ids are needed to construct
        subcorpuses for study objects to build proper topics.

        Args:
            interaction_name (str): The name of the interaction

        Returns:
            substudy_id (str): A textual representation of numeric Id for the substudy
            
        """

        substudy_id = super().get_from_section(interaction_name, 'substudy_mappings', 'substudy')

        return substudy_id

class StudyHelpers(BaseHelpers):
    def __init__(self, rewrite_rule_dir, obj_type='study'):
        super().__init__(rewrite_rule_dir, obj_type)

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
        for idx in list(self.rewrite_rules[section]):
            if introduction.match(idx): 
                document[intro]=self.rewrite_rules[section][idx]
            elif opportunities.match(idx):
                item_type=idx.split(seperator)[1]
                if item_type == 'Text': document['Opportunity']['text']=self.rewrite_rules[section][idx]
                else: document['Opportunity'][item_type]=self.rewrite_rules[section][idx]
            elif actions.match(idx):
                item_type=idx.split(seperator)[1]
                if item_type == 'Text': document['Action']['text']=self.rules[section][idx]
                else: document['Action'][item_type]=self.rewrite_rules[section][idx]
        return document

    def get_document (self, study_name, default='DEFAULT_PRFAQ'):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        section=self.util.reformat_name(study_name) + '_PRFAQ'
        document=self._document_helper(section) if self.rewrite_rules.has_section(section) else self._document_helper(default)
        return document

    # Transform either default or study specific questions into the proper data structure
    def _questions_helper(self, section, separator='|'):
        """Helper method for _get_questions to obtain, parse, format and return a question."""
        questions=dict()
        # to_skip=re.compile(self.to_skip, re.IGNORECASE)
        for idx in list(self.rewrite_rules[section]):
            # ./compa   if to_skip.match(idx): continue
            question=self.rewrite_rules[section][idx].split(separator)
            state=True if question[1] == 'True' else False
            questions[idx]={
                "question": question[0],
                "notes": question[2],
                "included": state
            }
        return questions

    # TODO the following section related to substudies, is in need of being significantly reworked.
    #       The immediate method below is an example which needs to be changed. One specific case
    #       is the 'get_substudy()' method that can be directly accessed here without needing to be
    #       passed in as an argument to the method.

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
    
    def _get_questions(self, study_name, substudy):
        """Internal method to obtain either the default set of questions or the study specific set of questions."""
        section=self.util.reformat_name(study_name) + '_Substudy_' + substudy + '_Questions'
        questions=self._questions_helper(section) if self.rewrite_rules.has_section(section) else dict()
        return questions

    def _noises_helper(self, section):
        """Helper method for _get_noises to obtain, parse, format and return the noises."""
        noises=dict()
        to_skip=re.compile(self.to_skip, re.IGNORECASE)
        for idx in list(self.rules[section]):
            if to_skip.match(idx): continue
            noise=self.rewrite_rules[section][idx]
            noises[idx]=noise
        return noises
    
    def _get_noises(self, study_name, substudy):
        """Internal method to obtain the set of study noises if they exist."""
        section=self.util.reformat_name(study_name) + '_Substudy_' + substudy + '_Noises'
        noises=self._noises_helper(section) if self.rewrite_rules.has_section(section) else dict()
        return noises

    def _get_substudy_type(self, study_name, substudy):
        section=self.util.reformat_name(study_name) + '_Substudy_Types'
        substudy_type=self.rewrite_rules.get(section, substudy) if self.rewrite_rules.has_option(section, substudy) else self.rewrite_rules.get('DEFAULT', 'substudy_type')
        return substudy_type

    # TODO reimplement according to the substudies construct in the backend
    def make_substudies(self, study, interaction_xform):
        theme_state=False # Define the default state of a substudy's theme; NOTE: should assign only after we detect if there are more than system assigned default themes
        final_substudies=dict() # Where we will store the final structure to be returned
        config_pre=self.util.reformat_name(study['studyName']) + '_Substudy_'

        # Process each substudy
        for substudy in study['substudies'].keys():
            definition=self.rules.get(config_pre + 'Definitions', substudy) if self.rules.has_section(config_pre + 'Definitions') else self.rules.get('DEFAULT', 'substudy_definition')
            name, description=definition.split('|')
            guid=self.util.hash_it(name + description) # For now set the GUID to be the combo of name and description, may be overidden by the DB in the future.
            final_substudies[substudy]={
                'type': self._get_substudy_type(study['studyName'], substudy),
                'totalInteractions': 0, # Set this sum to 0 # TODO deprecated
                'totalQuestions': 0, # Set this sum to 0 # TODO deprecated
                'totalThemes': 0, # Set this sum to 0 # TODO deprecated
                'noiseText': self._get_noises(study['studyName'], substudy),
                'name': name,
                'description': description,
                'GUID': guid, # TODO deprecated
                'interactions': self._get_interactions(study['linkedInteractions'], substudy, interaction_xform), # This needs to be reworked to get the substudy interactions
                'questions': self._get_questions(study['studyName'], substudy),
                'keyThemes': self._get_themes(study['studyName'], substudy), # TODO moved to be generated by caffeine, needed here?
                'keyThemeQuotes': self._get_theme_quotes(study['studyName'], substudy), # TODO moved to be generated by caffeine, needed here?
            }
            final_substudies[substudy]['totalInteractions']=self.util.total_item(final_substudies[substudy]['interactions']) # TODO deprecated
            final_substudies[substudy]['totalQuestions']=self.util.total_item(final_substudies[substudy]['questions']) # TODO deprecated
            final_substudies[substudy]['totalThemes']=self.util.total_item(final_substudies[substudy]['keyThemes']) # TODO deprecated
            if final_substudies[substudy]['totalThemes'] > 0: theme_state=True # TODO deprecated and this logic is not needed
            final_substudies[substudy]['themeState']=theme_state # TODO theme state should always be False at first ingest
        return final_substudies

class CompanyHelpers(BaseHelpers):
    def __init__(self, rewrite_rule_dir, obj_type='company'):
        super().__init__(rewrite_rule_dir, obj_type)
        self.DEFAULT_DOC = 'DEFAULT_PRFAQ'

    def _replace_company(self, text, company_name):
        text = text.strip()
        text = text.replace('\n', ' ')
        text = text.replace('$COMPANY$', company_name)
        return text

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
        for idx in list(self.rewrite_rules[section]):
            if introduction.match(idx):
                document[intro] = self.rewrite_rules[section][idx]
            elif purpose.match(idx):
                document[prps] = self.rewrite_rules[section][idx]
            elif actions.match(idx):
                item_type = idx.split(seperator)[1]
                if item_type == 'Text':
                    document['Action']['text'] = self.rewrite_rules[section][idx]
                else:
                    document['Action'][item_type] = self.rewrite_rules[section][idx]
        return document

    def get_document(self, company_name):
        """Pull the document from the rules if it exists.
        """

        # Create the section for the company doc
        my_section = self.util.reformat_name(company_name) + '_PRFAQ'

        # Check to see if the section exists otherwise revert to the default
        my_document = self._document_helper(my_section) if self.rewrite_rules.has_section(
            my_section) else self._document_helper(self.DEFAULT_DOC)

        # Format the document
        for doc_section in my_document.keys():
            my_text = my_document[doc_section]
            if type(my_text) is dict:
                for entry in my_text:
                    local_text = my_text[entry]
                    local_text = self._replace_company(local_text, company_name)
                    my_text[entry] = local_text
            else:
                my_text = self._replace_company(my_text, company_name)
            
            my_document[doc_section] = my_text
        return my_document
