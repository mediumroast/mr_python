__version__ = '1.0'
__author__  = "Michael Hay, John Goodman"
__date__    = '2021-September-12'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

import re
import boto3
from urllib.parse import urlparse
from urllib.parse import unquote
from botocore.client import Config

from ..helpers import utilities

class Extract:
    def __init__ (self, url='http://192.168.1.42:9000', access='medium_roast_io', secret='b7d1ac5ec5c2193a7d6dd61e7a8a76451885da5bd754b2b776632afd413d53e7', bucket='interactions', debug=False):
        self.s3=boto3.resource('s3',
                            endpoint_url=url,
                            aws_access_key_id=access,
                            aws_secret_access_key=secret,
                            config=Config(signature_version='s3v4'),
                            region_name='in-the-closet')
        
        # This imports the local utilies from mr_sdk for Python
        self.util=utilities()
        self.BUCKET=bucket
        self.BASE_URL=url.replace('http', 's3')
        self.DEBUG=debug

    def _get_index (self, resource):
        """Internal method to remove the object's extension and return the name with the hash."""
        obj_name = resource.split ('.')[0]
        return obj_name, self.util.hash_it(obj_name)

    def _get_objects(self):
        """Internal method to obtain all objects """
        entry_dict=dict()
        thumb_regex = re.compile ('^thumb_')
        my_bucket=self.s3.Bucket(self.BUCKET)
        for obj in my_bucket.objects.all():
            if self.DEBUG: print('Object key>>> ' + obj.key)
            obj_name, obj_hash=self._get_index(obj.key)
            if self.DEBUG: print('Object name>>> ' + obj_name)
            if thumb_regex.match(obj_name):
                obj_name=obj_name.replace ('thumb_', '')
                obj_hash=self.util.hash_it(obj_name)
                entry_dict[obj_hash].append(self.BASE_URL + '/' + self.BUCKET + '/' + obj.key)
            else:
                if thumb_regex.match(obj.key): continue
                
                entry_dict[obj_hash]=obj_name.split ('-')
                entry_dict[obj_hash].append(self.BASE_URL + '/' + self.BUCKET + '/' + obj.key)
        return list(entry_dict.values ()) # unwind the dict into a list and return


    def get_data (self):
        """Using the attributes set when the object was constructed get the data from the s3 bucket.

        Tested connectivity support:
            Minio: When creating open shares in Minio if the the output sent to STDOUT is captured in a file
                this utility will read the file format, extract the relevant data and return a list as prescribed below.

        Returns:
            list: A list of dicts which can be further processed
        """
        return self._get_objects()