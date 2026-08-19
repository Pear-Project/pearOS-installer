// Citește /etc/os-release la runtime, ca UI-ul să afișeze numele real al
// distribuției instalate (ex: "pearOS Goldwing") în loc de un nume hardcodat.
(function () {
  var fs = require('fs');

  function parseOsRelease(content) {
    var data = {};
    content.split('\n').forEach(function (line) {
      var m = line.match(/^([A-Z_]+)=(.*)$/);
      if (!m) return;
      var value = m[2].trim();
      if (value.length >= 2 && value[0] === '"' && value[value.length - 1] === '"') {
        value = value.slice(1, -1);
      }
      data[m[1]] = value;
    });
    return data;
  }

  function readOsRelease() {
    var paths = ['/etc/os-release', '/usr/lib/os-release'];
    for (var i = 0; i < paths.length; i++) {
      try {
        return parseOsRelease(fs.readFileSync(paths[i], 'utf8'));
      } catch (e) {}
    }
    return {};
  }

  var raw = readOsRelease();

  var OSRelease = {
    id: raw.ID || 'pearos',
    name: raw.NAME || 'pearOS',
    prettyName: raw.PRETTY_NAME || raw.NAME || 'pearOS',
    version: raw.VERSION || '',
    versionCodename: raw.VERSION_CODENAME || '',
    buildId: raw.BUILD_ID || '',
    imageId: raw.IMAGE_ID || '',
    imageVersion: raw.IMAGE_VERSION || '',
    logo: raw.LOGO || '',
    homeUrl: raw.HOME_URL || '',
    documentationUrl: raw.DOCUMENTATION_URL || '',
    supportUrl: raw.SUPPORT_URL || '',
    bugReportUrl: raw.BUG_REPORT_URL || ''
  };

  // Numele hardcodat cu care a fost livrat inițial acest installer, ca să
  // poată fi înlocuit oriunde apare cu numele real al distribuției curente.
  var LEGACY_NAME_PATTERN = /pearOS\s+NiceC0re/g;

  OSRelease.rebrand = function (text) {
    if (typeof text !== 'string') return text;
    return text.replace(LEGACY_NAME_PATTERN, OSRelease.prettyName);
  };

  window.OSRelease = OSRelease;
})();
