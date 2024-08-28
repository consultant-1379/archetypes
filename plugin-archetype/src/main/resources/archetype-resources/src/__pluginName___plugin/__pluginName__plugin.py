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
#from litp.core.validators import ValidationError
#from litp.core.task import ConfigTask

from litp.core.litp_logging import LitpLogger
log = LitpLogger()


class ${pluginClassname}Plugin(Plugin):
    """
    LITP ${pluginName} plugin
    """

    def validate_model(self, plugin_api_context):
        """
        This method can be used to validate the model ...

        .. warning::
          Please provide a summary of the model validation performed by
          ${pluginName} here
        """
        errors = []
#        nodes = plugin_api_context.query("node")
#        for node in nodes:
#            if node.hostname == "NOT_ALLOWED":
#                errors.append(ValidationError(
#                                item_path=node.get_vpath(),
#                                error_message="hostname cannot "
#                                "be 'NOT_ALLOWED'"
#                              ))
        return errors

    def create_configuration(self, plugin_api_context):
        """
        Plugin can provide tasks based on the model ...

        *Example CLI for this plugin:*

        .. code-block:: bash

          # TODO Please provide an example CLI snippet for plugin ${pluginName}
          # here
        """
        tasks = []

#        nodes = plugin_api_context.query("node")
#        for node in nodes:
#            if node.hostname == "special":
#                tasks.append(ConfigTask(node,
#                                       node.items.vim,
#                                       "Install vim on special node",
#                                       "package", "vim",
#                                       ensure="latest"
#                                       )
#                             )
        return tasks
