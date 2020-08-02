'''
Send an HTTP POST request to the online SBOL conversion tool
'''
import requests
from requests.exceptions import HTTPError
import json
import sys
import logging
import os
import GUI

def convert(genbank, output_fn = None, prefix="https://synbiohub.org/public/igem/", validator_url = 'https://validator.sbolstandard.org/validate/'):
    '''
    Converts a local genbank file to a sbol file.
    Input: GenBank filename, output_filename (Optional)
    Output: Converted SBOL file.
    '''

    file = open(genbank).read()
    request = { 'options': {'language' : 'SBOL2',
                            'test_equality': False,
                            'check_uri_compliance': False,
                            'check_completeness': False,
                            'check_best_practices': False,
                            'fail_on_first_error': False,
                            'provide_detailed_stack_trace': False,
                            'subset_uri': '',
                            'uri_prefix': prefix,
                            'version': '',
                            'insert_type': False,
                            'main_file_name': 'main file',
                            'diff_file_name': 'comparison file',
                                    },
                'return_file': True,
                'main_file': file
            }
    try:
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

        resp = requests.post(validator_url, json=request)
        # If the response was successful, no Exception will be raised
        resp.raise_for_status()
        resp = json.loads(resp.text)

        r = requests.get(resp["output_file"])
        GUI.successful_conversion()

        if output_fn is None:
            output_fn = genbank.split(os.path.sep)[-1].split(".")[0] + ".xml"
        
        if os.path.isdir(output_fn):
            os.remove(output_fn)

        with open(output_fn,"a") as file:
            file.write(r.text)

        return r.text





    except HTTPError as http_err:
        GUI.conversion_failure()
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        GUI.conversion_failure()
        print(f'Other error occurred: {err}')  # Python 3.6

if __name__ == '__main__':
    response = convert(sys.argv[1])
