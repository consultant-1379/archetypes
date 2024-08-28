#
# This file is to be used as a reference
# To setup the config dictionary in your plugin
#

# supported validation methods
validation_methods = [
    'ensure_unique',
    'ensure_only_one',
]

# supported call_id values
call_id_values = [
    'item_id',
    'item_path',
    'property_of_the_item',
]

# example plugin config
config = {
    'validations': [
        {'method': 'ensure_unique',
         'type': 'example-item',
         'property': 'prop1',
        },
        {'method': 'ensure_only_one',
         'type': 'example-item',
        },
    ],
    'configurations': [
        {'type': 'example-item',
         'call_type': 'example::config',
         'call_id': 'item_id',
         'configure': {
            'properties_to_add': {"ensure": "present"},
            'properties_to_rename': {'prop1':'prop2'},
            'properties_as_list': ["list_prop"],
            'properties_from_collection': [
                                           {'name': 'options',
                                            'key': 'option_name',
                                            'value': 'option_value',
                                           },
                                           {'name': "list_options",
                                            'key': 'option_name',
                                            'value': 'option_value',
                                            'value_as_list': True,
                                           },
                                          ],
          },
         'removal': {
            'properties_to_add': {"ensure": "absent"},
            'properties_to_drop': ["prop1"],
          },
        },
        {'type': 'example-item2',
         'call_type': 'example::config2',
         'call_id': 'prop1',
         'configure': {
            'properties_to_add': {"ensure": "present"},
            'properties_to_rename': {'prop1':'prop2'}
          },
         'removal': {
            'properties_to_add': {"ensure": "absent"},
            'properties_to_drop': ["prop1"],
          }
        },
    ],
}
