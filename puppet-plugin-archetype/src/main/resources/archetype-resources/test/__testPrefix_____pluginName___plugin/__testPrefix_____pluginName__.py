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

from ${pluginName}_plugin.${pluginName}plugin import ${pluginClassname}Plugin
from ${pluginName}_plugin import ${pluginName}plugin as plug

from litp.extensions.core_extension import CoreExtension
from litp.core.model_manager import ModelManager, QueryItem
from litp.core.plugin_manager import PluginManager
from litp.core.model_type import ItemType, Property, Collection
from litp.core.model_item import ModelItem
from litp.core.plugin_context_api import PluginApiContext
from mock import Mock

import unittest


class Test${pluginClassname}Plugin(unittest.TestCase):

    def setUp(self):
        """
        Construct a model, sufficient for test cases
        that you wish to implement in this suite.
        """
        self.model = ModelManager()
        self.context = PluginApiContext(self.model)
        self.model.register_property_types(
            CoreExtension().define_property_types())
        self.model.register_item_types(
            CoreExtension().define_item_types())
        self.model.create_root_item("root", "/")
        self.plugin = ${pluginClassname}Plugin()

    def setup_base_model(self):
        self.model.create_item('deployment', '/deployments/d1')
        self.model.create_item('cluster', '/deployments/d1/clusters/c1')
        self.node1 = self.model.create_item("node",
            '/deployments/d1/clusters/c1/nodes/n1',
            hostname="node1")
        self.assertEqual(ModelItem, type(self.node1))

    def register_example_software_item(self):
        self.model.register_item_type(ItemType("db-option",
                                               option_name=Property("basic_string"),
                                               option_value=Property("basic_string"),
                                               )
                                      )
        self.model.register_item_type(ItemType("user-option",
                                               option_name=Property("basic_string"),
                                               option_value=Property("basic_list"),
                                               )
                                      )
        self.model.register_item_type(ItemType("example-item",
                                               extend_item='software-item',
                                               prop1=Property("basic_string"),
                                               list_prop=Property("basic_list"),
                                               options=Collection("db-option"),
                                               user_options=Collection("user-option")
                                               )
                                      )

    def setup_model_with_example_item(self):
        self.setup_base_model()
        self.register_example_software_item()
        self.model.create_item('example-item',
            '/software/items/e1', prop1='abc', list_prop="a,b,c")
        self.model.create_item('db-option',
                               '/software/items/e1/options/opt1',
                               option_name='abc',
                               option_value="asdf")
        self.item1 = self.model.create_inherited(
            '/software/items/e1',
            '/deployments/d1/clusters/c1/nodes/n1/items/e1')
        self.assertEqual(ModelItem, type(self.item1))
        self.setup_plugin_config_1()

    def add_duplicate_example_item(self):
        self.item1 = self.model.create_inherited(
            '/software/items/e1',
            '/deployments/d1/clusters/c1/nodes/n1/items/e2')
        self.assertEqual(ModelItem, type(self.item1))

    def setup_model_with_example_cluster_item(self):
        self.setup_base_model()
        self.register_example_software_item()
        self.model.create_item('example-item',
                               '/software/items/e1', prop1='abc',
                               list_prop="def")
        self.model.create_item('user-option',
                               '/software/items/e1/user_options/opt1',
                               option_name='abc',
                               option_value="aaa,bbb")
        self.model.create_item(
            'clustered-service', '/deployments/d1/clusters/c1/services/s1',
            name='s1', active='1', standby='1', node_list='n1')
        self.model.create_item('runtime-entity',
            '/deployments/d1/clusters/c1/services/s1/runtimes/r1')

        self.item1 = self.model.create_inherited(
            '/software/items/e1',
            '/deployments/d1/clusters/c1/services/s1/runtimes/r1/packages/e1')
        self.assertEqual(ModelItem, type(self.item1))
        self.assertEqual(ModelItem, type(self.item1))
        self.assertEqual(ModelItem, type(self.item1))
        self.setup_plugin_config_1()

    def setup_plugin_config_1(self):
        plug.config = {
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
                                           {'name': "user_options",
                                            'key': 'option_name',
                                            'value': 'option_value',
                                            'value_as_list': True,
                                           },
                                      ]
                  },
                 'removal': {
                    'properties_to_add': {"ensure": "absent"},
                    'properties_to_drop': ["prop1"],
                  }
                },
            ],
        }

    def test_validate_model_no_errors_with_no_model(self):
        errors = self.plugin.validate_model(self.context)
        self.assertEqual(0, len(errors))

    def test_validate_model_no_errors_with_valid_model(self):
        self.setup_model_with_example_item()
        errors = self.plugin.validate_model(self.context)
        self.assertEqual(0, len(errors))

    def test_validate_model_unquie__and_only_one_errors_invalid_model(self):
        self.setup_model_with_example_item()
        self.add_duplicate_example_item()
        errors = self.plugin.validate_model(self.context)
        self.assertEqual(4, len(errors))
        error_paths = [error.item_path for error in errors]
        self.assertEqual(['/deployments/d1/clusters/c1/nodes/n1/items/e1',
                          '/deployments/d1/clusters/c1/nodes/n1/items/e2',
                          '/deployments/d1/clusters/c1/nodes/n1/items/e1',
                          '/deployments/d1/clusters/c1/nodes/n1/items/e2'],
                         error_paths)
        error_messages = [error.error_message for error in errors]
        self.assertEqual(['Property "prop1" with value "abc" is not unique on node "node1"',
                          'Property "prop1" with value "abc" is not unique on node "node1"',
                          'More than one item of type "example-item" on node "node1"',
                          'More than one item of type "example-item" on node "node1"'],
                         error_messages)

    def test_validate_model_no_errors_with_valid_cluster_model(self):
        self.setup_model_with_example_cluster_item()
        errors = self.plugin.validate_model(self.context)
        self.assertEqual(0, len(errors))

    def test_create_configuration_no_model_no_tasks(self):
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(0, len(tasks))

    def test_create_configuration_valid_model_1_task(self):
        self.setup_model_with_example_item()
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(1, len(tasks))
        task = tasks[0]
        # Assert the task is as expected
        self.assertEqual("/deployments/d1/clusters/c1/nodes/n1/items/e1",
                         task.model_item.get_vpath())
        self.assertEqual('Configure "e1" on node "node1"',
                         task.description)
        self.assertEqual("example::config", task.call_type)
        self.assertEqual("e1", task.call_id)
        self.assertEqual({'list_prop': ['a', 'b', 'c'],
                          'options': {'abc': 'asdf'},
                          "prop2": "abc",
                          "ensure": "present"}, task.kwargs)

    def test_create_configuration_valid_model_1_cluster_task(self):
        self.setup_model_with_example_cluster_item()
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(1, len(tasks))
        task = tasks[0]
        # Assert the task is as expected
        self.assertEqual(
           "/deployments/d1/clusters/c1/services/s1/runtimes/r1/packages/e1",
           task.model_item.get_vpath())
        self.assertEqual('Configure "e1" on node "node1"',
                         task.description)
        self.assertEqual("example::config", task.call_type)
        self.assertEqual("e1", task.call_id)
        self.assertEqual({'list_prop': ['def'],
                          'user_options': {'abc': ['aaa', 'bbb']},
                          "prop2": "abc",
                          "ensure": "present"}, task.kwargs)

    def test_create_configuration_all_applied_no_tasks(self):
        self.setup_model_with_example_item()
        self.model.set_all_applied()
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(0, len(tasks))

    def test_create_configuration_valid_model_update_tasks(self):
        self.setup_model_with_example_item()
        self.model.set_all_applied()
        self.model.update_item("/deployments/d1/clusters/c1/nodes/n1/items/e1",
            prop1="ghi")
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(1, len(tasks))
        task = tasks[0]
        # Assert the task is as expected
        self.assertEqual("/deployments/d1/clusters/c1/nodes/n1/items/e1",
                         task.model_item.get_vpath())
        self.assertEqual('Configure "e1" on node "node1"',
                         task.description)
        self.assertEqual("example::config", task.call_type)
        self.assertEqual("e1", task.call_id)
        self.assertEqual({'list_prop': ['a', 'b', 'c'],
                          'options': {'abc': 'asdf'},
                          "prop2": "ghi",
                          "ensure": "present"}, task.kwargs)

    def test_create_configuration_valid_model_removal_tasks(self):
        self.setup_model_with_example_item()
        self.model.set_all_applied()
        self.model.remove_item("/deployments/d1/clusters/c1/nodes/n1/items/e1")
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(1, len(tasks))
        task = tasks[0]
        # Assert the task is as expected
        self.assertEqual("/deployments/d1/clusters/c1/nodes/n1/items/e1",
                         task.model_item.get_vpath())
        self.assertEqual('Remove "e1" from node "node1"',
                         task.description)
        self.assertEqual("example::config", task.call_type)
        self.assertEqual("e1", task.call_id)
        self.assertEqual({'list_prop': 'a,b,c',
                          "ensure": "absent"}, task.kwargs)

    def test_get_call_id_with_item_id(self):
        mock_item = Mock()
        mock_item.item_id = "test_id"
        self.assertEqual('test_id',
                         self.plugin._get_call_id(mock_item, "item_id"))

    def test_get_call_id_with_property_id(self):
        mock_item = Mock()
        mock_item.item_id = "test_id"
        mock_item.properties = {"test_prop1": "prop_value1"}
        self.assertEqual('prop_value1',
                         self.plugin._get_call_id(mock_item, "test_prop1"))

    def test_get_call_id_with_item_path(self):
        mock_item = Mock()
        mock_item.item_id = "test_id"
        mock_item.properties = {"test_prop1": "prop_value"}
        mock_item.item_path = "/abc/def/ghi"
        self.assertEqual('_abc_def_ghi',
                         self.plugin._get_call_id(mock_item, "item_path"))

    def test_get_call_id_with_string_defaults_to_that_string(self):
        mock_item = Mock()
        mock_item.item_id = "test_id"
        mock_item.properties = {"test_prop1": "prop_value1"}
        self.assertEqual('random_string',
                         self.plugin._get_call_id(mock_item, "random_string"))
