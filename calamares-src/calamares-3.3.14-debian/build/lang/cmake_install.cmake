# Install script for directory: /home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/lang

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ar/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ar/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/as/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/as/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ast/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ast/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/az/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/az/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/az_AZ/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/az_AZ/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/be/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/be/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/bg/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/bg/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/bn/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/bn/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ca/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ca/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ca@valencia/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ca@valencia/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/cs_CZ/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/cs_CZ/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/da/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/da/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/de/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/de/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/el/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/el/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/en_GB/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/en_GB/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/eo/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/eo/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/es/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/es/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/es_AR/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/es_AR/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/es_MX/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/es_MX/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/et/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/et/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/eu/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/eu/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/fa/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/fa/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/fi_FI/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/fi_FI/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/fr/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/fr/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/fur/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/fur/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/gl/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/gl/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/he/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/he/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/hi/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/hi/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/hr/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/hr/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/hu/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/hu/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/id/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/id/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/is/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/is/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/it_IT/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/it_IT/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ja/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ja/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ka/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ka/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ko/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ko/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/lt/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/lt/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ml/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ml/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/mr/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/mr/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/nb/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/nb/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/nl/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/nl/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/oc/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/oc/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/pl/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/pl/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/pt_BR/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/pt_BR/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/pt_PT/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/pt_PT/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ro/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ro/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/ru/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/ru/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/si/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/si/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/sk/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/sk/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/sl/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/sl/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/sq/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/sq/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/sr/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/sr/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/sr@latin/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/sr@latin/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/sv/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/sv/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/tg/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/tg/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/th/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/th/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/tr_TR/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/tr_TR/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/uk/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/uk/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/vi/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/vi/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/zh_CN/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/zh_CN/LC_MESSAGES/calamares-python.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "CALAMARES" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/locale/zh_TW/LC_MESSAGES" TYPE FILE FILES "/home/alxb421/Desktop/pearOS-installer/calamares-src/calamares-3.3.14-debian/build/lang/zh_TW/LC_MESSAGES/calamares-python.mo")
endif()

