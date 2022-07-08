__version__ = '1.0'
__author__  = "Michael Hay, John Goodman"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."
import sys
sys.path.append('../')

from urllib.parse import urlparse
from urllib.parse import unquote
from ..helpers import utilities
import re, os


class Extract:
    """Perform raw data extract from a series of file types that contain links to a list of content.

    Args:
        filename (str): The fully qualified path/filename combination to pull in
            (default is './share_list.txt')
        source_type (str): Specify the type of file to import from.  Right now only an output derived from shares on Minio
            is supported. (default is 'minio')

    Returns:
        list: A list of dicts which can be further processed

    Methods:
        get_data()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__ (self, filename='./share_list.txt', source_type='minio'):
        self.file_resource=filename
        self.source_flavor=source_type

        # This imports the local utilies from mr_sdk for Python
        self.util=utilities()

    ### Internal helper methods

    # NOTE Unsure if this is a generic function required and therefore should be pushed to helpers
    def _getIndex (self, resource):
        """Internal method to pull out the file name from the path and return the file name plus its hash."""
        path = urlparse (resource).path
        file_name = (os.path.basename (path)).strip ()
        file_name = file_name.split ('.')[0]
        return file_name, self.util.hash_it(file_name)

    ### Drivers for various file types

    def _minio (self):
        """Internal 'driver' method to extract data from the Minio formated input file."""
        entry_dict={}
        url=""
        url_regex = re.compile ('^URL:')
        share_regex = re.compile ('^Share:')
        thumb_regex = re.compile ('^thumb_')
        with open (self.file_resource, 'r') as f:
            for file in f.readlines ():
                if url_regex.match (file):
                    url = file.strip ('URL: ')
                    (file_name, file_hash) = self._getIndex (url) # Clean up the file name and hash it
                    if thumb_regex.match (file_name): continue # Skip thumb_
                    entry_dict[file_hash] = file_name.split ('-') # Separate out the metadata
                elif share_regex.match (file):
                    share = unquote (file.strip ('Share:')).strip ()
                    (file_name, file_hash) = self._getIndex (share)
                    if thumb_regex.match (file_name): # Detect if this is a thumbnail
                        file_name = file_name.replace ('thumb_', '')
                        file_hash = self.util.hash_it (file_name)
                        entry_dict[file_hash].append (share) # Append the thumbnail
                    else:
                        entry_dict[file_hash].append (share) # Append the interaction resource
            f.close ()
        return list (entry_dict.values ()) # unwind the dict into a list and return

    
    def get_data (self):
        """Using the attributes set when the object was constructed get the data from the file.

        Current driver support:
            Minio: When creating open shares in Minio if the the output sent to STDOUT is captured in a file
                this utility will read the file format, extract the relevant data and return a list as prescribed below.

        Returns:
            list: A list of dicts which can be further processed
        """
        if self.source_flavor == 'minio': return self._minio()