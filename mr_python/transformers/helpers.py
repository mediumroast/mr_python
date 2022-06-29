__version__ = '1.0'
__author__ = "Michael Hay"
__date__ = '2022-June-11'
__copyright__ = "Copyright 2022 Mediumroast, Inc. All rights reserved."

# Perform key imports
import configparser as conf

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
        obj_name = self.rewrite_rules['names'][raw_name] if raw_name in self.rewrite_rules['names'] else raw_name

        return obj_name

    def get_description(self, raw_name):
        """Using the 'raw_name' of the object return a unique description, if it exists, otherwise return the default.

        In a rewrite rules file there is a [descriptions] section with 'raw_name=description' set.
        This method will take in 'raw_name' and return 'description'.  If there is no
        match for 'raw_name' in the section then the description from the [DEFAULT] section will be returned. 
        """

        # Return the rewritten description if it exists otherwise return the DEFAULT description
        return self.get_from_section(raw_name, 'descriptions', 'description')

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

        obj_value = self.rewrite_rules[section][name] if name in self.rewrite_rules[section] else self.rewrite_rules[default_section][default_name]

        return obj_value

class InteractionHelpers(BaseHelpers):
    def __init__(self, rewrite_rule_dir, obj_type='interaction'):
        super().__init__(rewrite_rule_dir, obj_type)

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

    def get_description(self, study_name, company_name, name=None):
        """Create a description from the interaction.

        Using a default in the configuration file merge in company and study names to generate a description for 
        the interaction.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A generated textual description generated from the company and study names.
        """
        # Get the generic description
        blank_description = super().get_description(name)
        description = blank_description.replace("COMPANY", str(company_name))
        return description.replace("STUDYNAME", str(study_name))
