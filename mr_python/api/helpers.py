# TODO this has been deprecated and should be removed

import hashlib

def hash_it(self, stringToHash, HASH='sha256'):
        h = hashlib.new (HASH)
        h.update (stringToHash.encode('utf-8'))
        return h.hexdigest ()

def save (self, file_name, string_data):
    """ Save string content to a file
    """
    with open(file_name, 'w') as my_file:
        try:
            my_file.write(string_data)
        except IOError as err:
            return False, err
        except:
            return False, 'Something went wrong, check the file output.'
        finally:
            return True, 'Successfully wrote the data to [' + file_name +']'