__version__ = '1.0'
__author__  = "Michael Hay, John Goodman"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

import os, magic

class Extract:
    """Perform raw data extract from a directory containing a listing of file names with included metadata

    Args:
        directory_name (str): The fully qualified path name 
            (default is '../../sample_data/sample_dir')

    Returns:
        list: A list of dicts which can be further processed

    Methods:
        get_data()
            Using the attributes set when the object was constructed get the data from the directory.

    """

    def __init__ (self, dir_name='../../sample_data/sample_dir', base_url='file://'):
        self.folder = dir_name
        self.base_url = base_url

    ### Internal helper methods

    # TODO this is likely broken and the format is potentially incorrect therefore it needs to be fixed and tested
    # NOTE Follow the s3bucket module as it includes intelligence on handling thumbnails

    def get_data (self):
            """Read content from a folder to extract key metadata from file names
            """
            items = []
            url = ""
            # Fall back to gathering data from the file system
            files = os.listdir (self.folfer)
            url = self.base_url + self.folder
            for file in files:
                raw_file = file
                file = file.split('.')[0] # remove the .extension
                entry = file.split ('-') # get the raw data
                entry.append (url + raw_file)
                items.append (entry)
            return items


        