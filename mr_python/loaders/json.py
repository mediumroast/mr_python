import json
from mr_python.helpers import utilities
__version__ = '1.0'
__author__ = "Michael Hay, John Goodman"
__date__ = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."


class Store:
    """Store data into a JSON formatted file assuming the input is a python object that can be serialized as proper JSON.

    Args:
        filename (str): The fully qualified filename to write the JSON to (default is '/tmp/mr_db.json')

    Returns:
        boolean: True or false depending on the success or failure of writing out the JSON file
        string: A string stating the status of the file write

    Methods:
        get_data()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__(self, filename='/tmp/mr_db.json', debug=False, indent=4):
        self.FILE = filename
        self.INDENT = indent

        # This imports the local utilies from mr_sdk for Python
        self.util = utilities()

    def persist(self, objs):
        success, result = self.util.save(
            self.FILE, json.dumps(objs, indent=self.INDENT))
        return success, result
