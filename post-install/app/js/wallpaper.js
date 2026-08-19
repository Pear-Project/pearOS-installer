// Preia fundalul curent setat în KDE Plasma al utilizatorului și îl aplică
// ca fundal al aplicației (în loc de imaginea statică din resources/),
// prin variabila CSS --wallpaper (vezi assistant-styles.css).
(function () {
  var fs = require('fs');
  var path = require('path');
  var os = require('os');

  // Extrage Image= dintr-o secțiune INI ale cărei chei de secțiune se termină
  // exact cu `sectionSuffix` (ex: "Wallpaper][org.kde.image][General" pentru
  // formatul din plasma-org.kde.plasma.desktop-appletsrc, sau "Wallpaper"
  // pentru formatul flat din pachetele Look-and-Feel).
  function readImageFromIniFile(filePath, sectionSuffix) {
    var content;
    try {
      content = fs.readFileSync(filePath, 'utf8');
    } catch (e) {
      return null;
    }

    var lines = content.split('\n');
    var inSection = false;
    var found = null;
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      var sectionMatch = line.match(/^\[(.+)\]$/);
      if (sectionMatch) {
        inSection = sectionMatch[1] === sectionSuffix || sectionMatch[1].indexOf(']' + sectionSuffix) !== -1 || sectionMatch[1].slice(-sectionSuffix.length) === sectionSuffix;
        continue;
      }
      if (inSection) {
        var m = line.match(/^Image=(.*)$/);
        // Prima valoare găsită e suficientă pentru un fundal reprezentativ.
        if (m && !found) found = m[1].trim();
      }
    }
    return found;
  }

  // Config-ul per-utilizator, dacă a schimbat vreodată wallpaper-ul explicit.
  function readUserWallpaperOverride() {
    var configPath = path.join(os.homedir(), '.config', 'plasma-org.kde.plasma.desktop-appletsrc');
    return readImageFromIniFile(configPath, 'Wallpaper][org.kde.image][General');
  }

  // Dacă nu există override, wallpaper-ul vine din tema Look-and-Feel (Global
  // Theme) activă — nescris niciodată explicit în config-ul de mai sus.
  function readLookAndFeelWallpaper() {
    var kdeglobals = path.join(os.homedir(), '.config', 'kdeglobals');
    var content;
    try {
      content = fs.readFileSync(kdeglobals, 'utf8');
    } catch (e) {
      return null;
    }
    var m = content.match(/^LookAndFeelPackage=(.+)$/m);
    if (!m) return null;
    var themeId = m[1].trim();

    var defaultsPaths = [
      path.join(os.homedir(), '.local/share/plasma/look-and-feel', themeId, 'contents/defaults'),
      path.join('/usr/share/plasma/look-and-feel', themeId, 'contents/defaults')
    ];
    for (var i = 0; i < defaultsPaths.length; i++) {
      var val = readImageFromIniFile(defaultsPaths[i], 'Wallpaper');
      if (val) return val;
    }
    return null;
  }

  function fileUriToPath(uri) {
    if (uri.indexOf('file://') === 0) {
      try {
        return decodeURIComponent(uri.slice('file://'.length));
      } catch (e) {
        return uri.slice('file://'.length);
      }
    }
    return uri;
  }

  // O valoare Image= poate fi: un file:// URI, o cale absolută, sau doar
  // id-ul pachetului de wallpaper (ex: "Next") căutat în directoarele
  // standard de wallpapers.
  function candidatePaths(value) {
    if (value.indexOf('file://') === 0 || value.indexOf('/') === 0) {
      return [fileUriToPath(value)];
    }
    return [
      path.join(os.homedir(), '.local/share/wallpapers', value),
      path.join('/usr/share/wallpapers', value)
    ];
  }

  // Pachetele de wallpaper KDE sunt directoare cu mai multe rezoluții în
  // contents/images/; alegem cea mai mare disponibilă.
  function resolveImageFile(p) {
    var stat;
    try {
      stat = fs.statSync(p);
    } catch (e) {
      return null;
    }
    if (stat.isFile()) return p;
    if (!stat.isDirectory()) return null;

    var imagesDir = path.join(p, 'contents', 'images');
    var candidates;
    try {
      candidates = fs.readdirSync(imagesDir);
    } catch (e) {
      return null;
    }
    if (candidates.length === 0) return null;

    candidates.sort(function (a, b) {
      function area(name) {
        var m = name.match(/(\d+)x(\d+)/);
        return m ? parseInt(m[1], 10) * parseInt(m[2], 10) : 0;
      }
      return area(b) - area(a);
    });
    return path.join(imagesDir, candidates[0]);
  }

  function resolveWallpaper(value) {
    var candidates = candidatePaths(value);
    for (var i = 0; i < candidates.length; i++) {
      var resolved = resolveImageFile(candidates[i]);
      if (resolved) return resolved;
    }
    return null;
  }

  function toFileUrl(p) {
    return 'file://' + p.split(path.sep).map(encodeURIComponent).join('/');
  }

  var raw = readUserWallpaperOverride() || readLookAndFeelWallpaper();
  if (!raw) return;

  var resolved = resolveWallpaper(raw);
  if (!resolved) return;

  document.documentElement.style.setProperty('--wallpaper', 'url("' + toFileUrl(resolved) + '")');
})();
