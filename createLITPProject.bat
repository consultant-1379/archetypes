rem @echo off

set EXTENSION=extension
set PLUGIN=plugin
set PUPPET_EXTENSION=puppet-extension
set PUPPET_PLUGIN=puppet-plugin
set PUPPET_MODULE=puppet
set LIBRARY=library

set TYPE=%1

rem echo %TYPE%

if "%TYPE%" == "%EXTENSION%"  (
    echo \n### Generating extension %2
    set EXTENSION_NAME=%2
    set EXTENSION_CLASSNAME=%3
    set EXTENSION_CXP=%4
    mvn.bat archetype:generate -DarchetypeCatalog=local -DartifactId=ERIClitp%EXTENSION_NAME%api ^
    -DcxpNumber=%EXTENSION_CXP% -DextensionName=%EXTENSION_NAME% -DextensionClassname=%EXTENSION_CLASSNAME% ^
    -DarchetypeGroupId=com.ericsson.nms.litp -DarchetypeArtifactId=litp-extension-archetype -DinteractiveMode=false
    goto end
)
if "%TYPE%" == "%PUPPET_EXTENSION%" (
    echo \n### Generating puppet-extension %2
    set EXTENSION_NAME=%2
    set EXTENSION_CLASSNAME=%3
    set EXTENSION_CXP=%4
    mvn.bat archetype:generate -DarchetypeCatalog=local -DartifactId=ERIClitp%EXTENSION_NAME%api ^
    -DcxpNumber=%EXTENSION_CXP% -DextensionName=%EXTENSION_NAME% -DextensionClassname=%EXTENSION_CLASSNAME% &
    -DarchetypeGroupId=com.ericsson.nms.litp -DarchetypeArtifactId=litp-puppet-extension-archetype -DinteractiveMode=false
    goto end
)
if "%TYPE%" == "%PLUGIN%" (
    echo \n### Generating plugin %2
    set PLUGIN_NAME=%2
    set PLUGIN_CLASSNAME=%3
    set PLUGIN_CXP=%4
    mvn.bat archetype:generate -DarchetypeCatalog=local -DartifactId=ERIClitp%PLUGIN_NAME% ^
    -DcxpNumber=%PLUGIN_CXP% -DpluginName=%PLUGIN_NAME% -DpluginClassname=%PLUGIN_CLASSNAME% ^
    -DarchetypeGroupId=com.ericsson.nms.litp -DarchetypeArtifactId=litp-plugin-archetype -DinteractiveMode=false
    goto end
)
if "%TYPE%" == "%PUPPET_PLUGIN%" (
    echo \n### Generating puppet-plugin %2
    set PLUGIN_NAME=%2
    set PLUGIN_CLASSNAME=%3
    set PLUGIN_CXP=%4
    mvn.bat archetype:generate -DarchetypeCatalog=local -DartifactId=ERIClitp%PLUGIN_NAME% ^
    -DcxpNumber=%PLUGIN_CXP% -DpluginName=%PLUGIN_NAME% -DpluginClassname=%PLUGIN_CLASSNAME% ^
    -DarchetypeGroupId=com.ericsson.nms.litp -DarchetypeArtifactId=litp-puppet-plugin-archetype -DinteractiveMode=false
    goto end
)
if "%TYPE%" == "%PUPPET_MODULE%" (
    echo \n### Generating puppet-module %2
    set MODULE_NAME=%2
    set MODULE_VERSION=%3
    set MODULE_CXP=%4
    mvn.bat archetype:generate -DarchetypeCatalog=local -DartifactId=EXTRlitppuppet%MODULE_NAME% ^
    -DcxpNumber=%MODULE_CXP% -DmoduleName=%MODULE_NAME% -DmoduleVersion=%MODULE_VERSION% ^
    -DarchetypeGroupId=com.ericsson.nms.litp -DarchetypeArtifactId=litp-puppet-archetype -DinteractiveMode=false
    goto end
)
if "%TYPE%" == "%LIBRARY%" (
    echo \n### Generating library %2
    set LIBRARY_NAME=%2
    set LIBRARY_CLASSNAME=%3
    set LIBRARY_CXP=%4
    mvn.bat archetype:generate -DarchetypeCatalog=local -DartifactId=ERIClitp%LIBRARY_NAME%lib ^
    -DcxpNumber=%LIBRARY_CXP% -DlibraryName=%LIBRARY_NAME% -DlibraryClassname=%LIBRARY_CLASSNAME% ^
    -DarchetypeGroupId=com.ericsson.nms.litp -DarchetypeArtifactId=litp-library-archetype -DinteractiveMode=false
    goto end
)
echo Usage: %0 plugin^|extension^|puppet-plugin^|puppet-extension^|library name classname cxp
echo Examples:
echo     %0 extension san SAN CXP1234567
echo     %0 plugin san SAN CXP1234567
echo     %0 library cba CBA CXP1234567
echo     %0 puppet firewall 1.0.2 CXP1234567
echo     %0 puppet-extension san SAN CXP1234567
echo     %0 puppet-plugin san SAN CXP1234567

:end
