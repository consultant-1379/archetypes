#
# This file is to be used as a reference
# To setup the config dictionary in your extension
#

# for all core property types, see: "https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/sites/litp2/ERIClitpdocs/latest/extensions/core_extension_extension/index.html#defined-property-types"
property_types = [
    'any_string',           # "^.*$"
    'basic_string',         # "^[a-zA-Z0-9\-\._]+$"
    'basic_list',           # "^[a-zA-Z0-9\-\._]*(,[a-zA-Z0-9\-\._]+)*$"
    'basic_boolean',        # "^(true|false)$"
    'path_string',          # "^/[A-Za-z0-9\-\._/#:\s*]+$"
    'file_path_string',     # "^[A-Za-z0-9\-\._/#:\s*]+$"
    'file_mode',            # "^[0-7]?[0-7][0-7][0-7]$"
    'digit',                # "^[0-9]$"
    'integer',              # "^[0-9]+$"
    'positive_integer',     # "^[1-9][0-9]*$"
    'port',                 # "^[0-9]+$"
    'hostname',
    'ipv4_address',
    'ipv6_address',
    'ipv6_address_and_mask',
    'ipv4_or_ipv6_address',
    'mac_address',          # "^([a-fA-F0-9]{2}(:|\-)){5}([a-fA-F0-9]{2})$"
    'disk_size',            # "^[1-9][0-9]{0,}[MGT]$"
    'disk_uuid',            # "^[a-zA-Z0-9_][a-zA-Z0-9_-]*$"
]

# example import for a Validator: "from litp.core.validators import ExampleValidator"
# for all core property validators, see: "https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/sites/litp2/ERIClitpdocs/latest/plugin_api/validators.html#prop-validators"
property_validators = [
    'DirectoryExistValidator(directory_path)',
    'PropertyLengthValidator(max_length)',
    'IntRangeValidator(min_value, max_value)',
    'RestrictedPropertiesValidator(restricted_values_list)'
]

# for all core item types, see: "https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/sites/litp2/ERIClitpdocs/latest/extensions/core_extension_extension/index.html#defined-item-types"
base_item_types = [
    'software-item',
    'service',
    'node-config',
    'cluster-config',
]

# for all item valiadtors, see: "https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/sites/litp2/ERIClitpdocs/latest/extensions/core_extension_extension/index.html#defined-item-types"
item_validators = [
    'OnePropertyValidator(property_names_list)',
    'MaxValueValidator(limit_property_name, property_to_limt_name)'
]

# example extension config
config = {
    'property_types': [
        {'id': 'example_property_type_id',
         'regex':  r"^[1-9][0-9]{0,}G$",
         'validators': [],
        },
    ],
    'item_types': [
        {'id': 'example-item-type',
         'extends': 'software-item',
         'description':  "Example item type.",
         'properties': [
            {'name': 'name',
             'type': 'basic_string',
             'description': 'Name of item.',
             'required': True,
             'default': 'abc',
             'validators': [],
            },
         ],
        'collections': [
            {'id': 'databases',
             'type': 'database-item',
             'min_count': 1,
             'max_count': 100,
            },
         ],
         'validators': [],
        },
    ],
}
