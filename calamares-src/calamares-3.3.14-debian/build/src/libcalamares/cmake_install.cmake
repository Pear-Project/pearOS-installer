# Install script for directory: /home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamares.so.3.3.14"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamares.so.3.3"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/libcalamares.so.3.3.14"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/libcalamares.so.3.3"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamares.so.3.3.14"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamares.so.3.3"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/libcalamares.so")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  
    file( MAKE_DIRECTORY "$ENV{DESTDIR}//usr/lib/calamares" )
    execute_process( COMMAND "/usr/bin/cmake" -E create_symlink ../libcalamares.so.3.3.14 libcalamares.so WORKING_DIRECTORY "$ENV{DESTDIR}//usr/lib/calamares" )

endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/src/libcalamares/CalamaresConfig.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/src/libcalamares/CalamaresVersion.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/CalamaresAbout.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/CppJob.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/DllMacro.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/GlobalStorage.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/Job.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/JobExample.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/JobQueue.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/ProcessJob.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/Settings.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/geoip" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/geoip/GeoIPFixed.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/geoip/GeoIPJSON.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/geoip/GeoIPTests.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/geoip/GeoIPXML.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/geoip/Handler.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/geoip/Interface.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/locale" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/locale/Global.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/locale/Lookup.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/locale/TimeZone.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/locale/TranslatableConfiguration.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/locale/TranslatableString.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/locale/Translation.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/locale/TranslationsModel.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/modulesystem" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/Actions.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/Config.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/Descriptor.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/InstanceKey.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/Module.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/Preset.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/Requirement.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/RequirementsChecker.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/modulesystem/RequirementsModel.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/network" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/network/Manager.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/network/Tests.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/partition" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/AutoMount.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/FileSystem.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/Global.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/KPMHelper.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/KPMManager.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/Mount.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/PartitionIterator.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/PartitionQuery.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/PartitionSize.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/partition/Sync.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/utils" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/CommandList.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Dirs.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Entropy.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Logger.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/NamedEnum.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/NamedSuffix.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Permissions.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/PluginFactory.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/RAII.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Retranslator.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Runner.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/String.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/StringExpander.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/System.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Traits.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/UMask.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Units.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Variant.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/Yaml.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/utils/moc-warnings.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/compat" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/compat/CheckBox.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/compat/Mutex.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/compat/Size.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/compat/Variant.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/compat/Xml.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/packages" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamares/packages/Globals.h")
endif()

