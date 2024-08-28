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

#from litp.core.model_type import ItemType, Property, PropertyType
from litp.core.extension import ModelExtension

from litp.core.litp_logging import LitpLogger
log = LitpLogger()


class ${extensionClassname}Extension(ModelExtension):
    """
    ${extensionClassname} Model Extension
    """

    def define_property_types(self):
        property_types = []
#        property_types.append(PropertyType("example_property_type",
#                                           regex="^[1-9][0-9]{0,}G$"),)
        return property_types

    def define_item_types(self):
        item_types = []
#        item_types.append(
#            ItemType("example-custom-item-type",
#                     extend_item="software-item",
#                     item_description="Example item type",
#                     name=Property("basic_string",
#                                   prop_description="Name of item",
#                                   required=True),
#                     size=Property("example_property_type",
#                                   prop_description="Size of item",
#                                   default="10G"),
#            )
#        )
        return item_types
