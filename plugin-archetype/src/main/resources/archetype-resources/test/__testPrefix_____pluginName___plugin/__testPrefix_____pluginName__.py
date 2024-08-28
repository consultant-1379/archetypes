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

from litp.extensions.core_extension import CoreExtension
from litp.core.model_manager import ModelManager, QueryItem
from litp.core.plugin_manager import PluginManager
from litp.core.model_type import ItemType, Child
from litp.core.plugin_context_api import PluginApiContext

import unittest


class Test${pluginClassname}Plugin(unittest.TestCase):

    def setUp(self):
        """
        Construct a model, sufficient for test cases
        that you wish to implement in this suite.
        """
        self.model = ModelManager()
        # Instantiate a plugin API context to pass to plugin
        self.context = PluginApiContext(self.model)
        self.plugin_manager = PluginManager(self.model)
        # Use add_property_types to add property types defined in 
        # model extenstions
        # For example, from CoreExtensions (recommended)
        self.plugin_manager.add_property_types(
            CoreExtension().define_property_types())

        # Use add_item_types to add item types defined in 
        # model extensions
        # For example, from CoreExtensions
        self.plugin_manager.add_item_types(
            CoreExtension().define_item_types())

        # Add default minimal model (which creates '/' root item)
        self.plugin_manager.add_default_model()

        # Instantiate your plugin and register with PluginManager
        self.plugin = ${pluginClassname}Plugin()

    def setup_model(self):
        # Use ModelManager.crete_item and ModelManager.create_inherited
        # to create and inherit items in the model.
        self.model.create_item('deployment', '/deployments/d1')
        self.model.create_item('cluster', '/deployments/d1/clusters/c1')
        self.node1 = self.model.create_item("node",
            '/deployments/d1/clusters/c1/nodes/n1', hostname="node1")
        self.node1 = self.model.create_item("node",
            '/deployments/d1/clusters/c1/nodes/n2', hostname="special")

    def test_validate_model(self):
        self.setup_model()
        # Invoke plugin's methods to run test cases 
        # and assert expected output.
        errors = self.plugin.validate_model(self.context)
        self.assertEqual(0, len(errors))

    def test_create_configuration(self):
        self.setup_model()
        # Invoke plugin's methods to run test cases 
        # and assert expected output.
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(0, len(tasks))
