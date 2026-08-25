# Install script for directory: /home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui

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
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamaresui.so.3.3.14"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamaresui.so.3.3"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/libcalamaresui.so.3.3.14"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/libcalamaresui.so.3.3"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamaresui.so.3.3.14"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libcalamaresui.so.3.3"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHANGE
           FILE "${file}"
           OLD_RPATH "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build:"
           NEW_RPATH "")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/libcalamaresui.so")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/Branding.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/ViewManager.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/modulesystem" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/modulesystem/CppJobModule.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/modulesystem/ModuleFactory.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/modulesystem/ModuleManager.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/modulesystem/ProcessJobModule.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/modulesystem/PythonJobModule.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/modulesystem/ViewModule.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/utils" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/utils/Gui.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/utils/ImageRegistry.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/utils/Paste.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/utils/Qml.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/utils/QtCompat.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/viewpages" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/viewpages/BlankViewStep.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/viewpages/ExecutionViewStep.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/viewpages/QmlViewStep.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/viewpages/Slideshow.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/viewpages/ViewStep.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libcalamares/widgets" TYPE FILE FILES
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/ClickableLabel.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/ErrorDialog.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/FixedAspectRatioLabel.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/LogWidget.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/PrettyRadioButton.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/TranslationFix.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/WaitingWidget.h"
    "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/src/libcalamaresui/widgets/waitingspinnerwidget.h"
    )
endif()

