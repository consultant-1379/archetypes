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

from litp.core.plugin import Plugin
from litp.core.validators import ValidationError
from litp.core.task import ConfigTask

from litp.core.litp_logging import LitpLogger
log = LitpLogger()

config = {
    'validations': [
    ],
    'configurations': [
    ],
}


class ${pluginClassname}Plugin(Plugin):
    """
    LITP ${pluginName} plugin
    """

    @staticmethod
    def _get_config(key):
        return config.get(key)

    @staticmethod
    def _all_nodes(api_context):
        nodes = api_context.query("node") + api_context.query("ms")
        return [node for node in nodes if not node.is_for_removal()]

    def _add_errors(self, api_context, validation, errors):
        if validation['method'] == "ensure_unique":
            validation_errors = self._ensure_unique(api_context, validation)
        elif validation['method'] == "ensure_only_one":
            validation_errors = self._ensure_only_one(api_context, validation)
        errors.extend(validation_errors)

    def _add_items_to_node_value_set(self, node, items,
                                     prop, items_by_value_by_node):
        if node not in items_by_value_by_node:
            items_by_value_by_node[node] = {}
        for item in items:
            value = getattr(item, prop)
            if value:
                items_list = items_by_value_by_node[node].get(value, [])
                items_list.append(item.get_vpath())
                items_by_value_by_node[node][value] = items_list

    def _ensure_unique(self, api_context, validation):
        items_by_value_by_node = {}
        item_type = validation['type']
        prop = validation['property']
        # standard node config items
        for node in self._all_nodes(api_context):
            items = node.query(item_type)
            self._add_items_to_node_value_set(
                node.hostname, items, prop, items_by_value_by_node)

        for cluster in api_context.query('cluster'):
            # cluster config items
            items = cluster.configs.query(item_type)
            for node in cluster.nodes:
                self._add_items_to_node_value_set(
                    node.hostname, items, prop, items_by_value_by_node)
            # clustered service config items
            for clustered_service in cluster.query('clustered-service'):
                items = clustered_service.query(item_type)
                for node in clustered_service.nodes:
                    self._add_items_to_node_value_set(
                        node.hostname, items, prop, items_by_value_by_node)

        return self._create_unique_errors(items_by_value_by_node, prop)

    def _create_unique_errors(self, items_by_value_by_node, prop):
        errors = []
        for node, items_by_value in items_by_value_by_node.items():
            for value, items in items_by_value.items():
                if len(set(items)) > 1:
                    for item_path in set(items):
                        errors.append(
                            ValidationError(
                                item_path=item_path,
                                error_message=(
                                'Property "%s" with value "%s" '
                                'is not unique on node "%s"'
                                % (prop, value, node)))
                        )
        return errors

    def _add_items_to_node_set(self, node, items, items_by_node):
        for item in items:
            items_list = items_by_node.get(node, [])
            items_list.append(item.get_vpath())
            items_by_node[node] = items_list

    def _ensure_only_one(self, api_context, validation):
        items_by_node = {}
        item_type = validation['type']
        # standard node config items
        for node in self._all_nodes(api_context):
            items = node.query(item_type)
            self._add_items_to_node_set(node.hostname, items, items_by_node)

        for cluster in api_context.query('cluster'):
            # cluster config items
            items = cluster.configs.query(item_type)
            for node in cluster.nodes:
                self._add_items_to_node_set(
                    node.hostname, items, items_by_node)
            # clustered service config items
            for clustered_service in cluster.services:
                items = clustered_service.query(item_type)
                for node in clustered_service.nodes:
                    self._add_items_to_node_set(
                        node.hostname, items, items_by_node)

        return self._create_only_one_errors(items_by_node, item_type)

    def _create_only_one_errors(self, items_by_node, item_type):
        errors = []
        for node, items_paths in items_by_node.items():
            if len(set(items_paths)) > 1:
                for item_path in set(items_paths):
                    errors.append(
                        ValidationError(
                            item_path=item_path,
                            error_message=(
                            'More than one item of type "%s" on node "%s"'
                            % (item_type,  node)))
                    )
        return errors

    def validate_model(self, api_context):
        """
        This method can be used to validate the model ...

        .. warning::
          Please provide a summary of the model validation performed by
          ${pluginName} here
        """
        errors = []
        for validation in self._get_config('validations'):
            self._add_errors(api_context, validation, errors)
        return errors

    def _add_tasks(self, node, items, configuration, tasks):
        for item in items:
            task = self._create_task(node, item, configuration)
            if task is not None:
                tasks.append(task)

    @staticmethod
    def _get_call_id(item, call_id_config):
        if call_id_config == 'item_id':
            return item.item_id
        elif call_id_config in item.properties:
            return item.properties[call_id_config]
        if call_id_config == 'item_path':
            return item.item_path.replace("/", '_')
        else:
            return call_id_config

    def _create_task(self, node, item, configuration):
        if item.is_initial() or item.is_updated():
            return ConfigTask(
                         node, item,
                         'Configure "%s" on node "%s"' % (item.item_id,
                                                          node.hostname),
                         configuration['call_type'],
                         self._get_call_id(item, configuration['call_id']),
                         **self._get_properties(
                                item, configuration['configure']
                                )
                   )
        elif item.is_for_removal() and 'removal' in configuration:
            return ConfigTask(
                         node, item,
                         'Remove "%s" from node "%s"' % (item.item_id,
                                                         node.hostname),
                         configuration['call_type'],
                         self._get_call_id(item, configuration['call_id']),
                         **self._get_properties(item,
                                                configuration['removal'])
                   )

    def _get_properties(self, item, configuration):
        properties = item.properties
        if item.is_for_removal():
            properties = item.applied_properties
        if 'properties_to_drop' in configuration:
            for prop in configuration['properties_to_drop']:
                if prop in properties:
                    del properties[prop]
        if 'properties_as_list' in configuration:
            list_props = configuration['properties_as_list']
            for list_prop in list_props:
                if list_prop in properties:
                    properties[list_prop] = \
                                self._to_list(properties[list_prop])
        if 'properties_to_add' in configuration:
            properties.update(configuration['properties_to_add'])
        if 'properties_to_rename' in configuration:
            renames = configuration['properties_to_rename']
            for from_property, to_property in renames.items():
                if from_property in properties:
                    properties[to_property] = properties[from_property]
                    del properties[from_property]
        if 'properties_from_collection' in configuration:
            from_collections = configuration['properties_from_collection']
            for from_collection in from_collections:
                collection = getattr(item, from_collection['name'])
                if collection and len(collection) > 0:
                    collection_props = {}
                    for coll_item in collection:
                        key = from_collection['key']
                        value_key = from_collection['value']
                        if "value_as_list" in from_collection:
                            prop_value = self._to_list(
                                             getattr(coll_item, value_key))
                        else:
                            prop_value = getattr(coll_item, value_key)
                        collection_props[getattr(coll_item, key)] = prop_value
                    properties[from_collection['name']] = collection_props
        return properties

    @staticmethod
    def _to_list(value):
        seperator = ','
        if seperator in value:
            list_value = value.split(seperator)
        else:
            list_value = [value]
        return list_value

    def create_configuration(self, api_context):
        """
        Plugin can provide tasks based on the model ...

        *Example CLI for this plugin:*

        .. code-block:: bash

          # TODO Please provide an example CLI snippet for plugin ${pluginName}
          # here
        """
        tasks = []
        for configuration in self._get_config('configurations'):
            # standard node config items
            for node in self._all_nodes(api_context):
                items = node.query(configuration['type'])
                self._add_tasks(node, items, configuration, tasks)

            for cluster in api_context.query('cluster'):
                # cluster config items
                items = cluster.configs.query(configuration['type'])
                for node in cluster.nodes:
                    self._add_tasks(node, items, configuration, tasks)
                # clustered service config items
                for clustered_service in cluster.services:
                    items = clustered_service.query(configuration['type'])
                    for node in clustered_service.nodes:
                        self._add_tasks(node, items, configuration, tasks)
        return tasks
