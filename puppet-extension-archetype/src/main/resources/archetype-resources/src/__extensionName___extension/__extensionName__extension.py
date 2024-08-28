#set( $H = '#' )
$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H
# COPYRIGHT Ericsson AB 2014
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H$H

from litp.core.model_type import Child, Collection, ItemType, \
                                 Property, PropertyType
from litp.core.extension import ModelExtension

from litp.core.litp_logging import LitpLogger
log = LitpLogger()

config = {
    'property_types': [
    ],
    'item_types': [
    ],
}


class ${extensionClassname}Extension(ModelExtension):
    """
    ${extensionClassname} Model Extension
    """
    @staticmethod
    def _get_config(key):
        return config.get(key)

    def _create_property_type(self, property_type_config):
        kwargs = {}
        self._dict_to_dict(property_type_config, 'regex', kwargs)
        self._dict_to_dict(property_type_config, 'validators', kwargs)
        return PropertyType(property_type_config['id'], **kwargs)

    def define_property_types(self):
        property_types = []
        for property_type_config in self._get_config('property_types'):
            property_type = self._create_property_type(property_type_config)
            property_types.append(property_type)
        return property_types

    def _dict_to_dict_keys(self, from_dict, keys, to_dict):
        for key in keys:
            self._dict_to_dict(from_dict, key, to_dict)

    @staticmethod
    def _dict_to_dict(from_dict, key, to_dict, to_key=None):
        """ Copy from one dict to another if present """
        if to_key is None:
            to_key = key
        if from_dict.get(key):
            to_dict[to_key] = from_dict[key]

    def _create_item_type(self, item_type_config):
        item_kwargs = {}
        self._dict_to_dict(item_type_config, 'extends',
                           item_kwargs, to_key='extend_item')
        self._dict_to_dict(item_type_config, 'description',
                           item_kwargs, to_key='item_description')
        if 'properties' in item_type_config:
            self._add_properties(item_type_config.get('properties'),
                                 item_kwargs)
        if 'collections' in item_type_config:
            self._add_collections(item_type_config.get('collections'),
                                  item_kwargs)
        if 'children' in item_type_config:
            self._add_children(item_type_config.get('children'),
                               item_kwargs)
        if 'validators' in item_type_config:
            item_kwargs['validators'] = item_type_config.get('validators')
        item_type = ItemType(item_type_config['id'], **item_kwargs)
        return item_type

    def _add_properties(self, properties, item_kwargs):
        for property_config in properties:
            property_item = self._create_property(property_config)
            item_kwargs[property_config['name']] = property_item

    def _create_property(self, property_config):
        property_kwargs = {}
        self._dict_to_dict(property_config, 'description',
                           property_kwargs, to_key='prop_description')
        pass_through_keys = ['default', 'required', 'deprecated',
                             'updatable_plugin', 'updatable_rest']
        self._dict_to_dict_keys(property_config, pass_through_keys,
                                property_kwargs)
        property_item = Property(property_config['type'], **property_kwargs)
        return property_item

    def _add_collections(self, collections, item_kwargs):
        for collection_config in collections:
            collection = self._create_collection(collection_config)
            item_kwargs[collection_config['id']] = collection

    def _create_collection(self, collection_config):
        collection_kwargs = {}
        pass_through_keys = ['min_count', 'max_count',
                             'require', 'deprecated']
        self._dict_to_dict_keys(collection_config, pass_through_keys,
                                collection_kwargs)
        collection_item = Collection(collection_config['type'],
                                     **collection_kwargs)
        return collection_item

    def _add_children(self, children, item_kwargs):
        for child_config in children:
            child = self._create_child(child_config)
            item_kwargs[child_config['id']] = child

    def _create_child(self, child_config):
        child_kwargs = {}
        pass_through_keys = ['require', 'deprecated']
        self._dict_to_dict_keys(child_config, pass_through_keys,
                                child_kwargs)
        child_item = Child(child_config['type'],
                           **child_kwargs)
        return child_item

    def define_item_types(self):
        item_types = []
        for item_type_config in self._get_config('item_types'):
            item_type = self._create_item_type(item_type_config)
            item_types.append(item_type)
        return item_types
