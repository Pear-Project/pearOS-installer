// Înlocuiește în DOM orice text hardcodat cu numele real al distribuției
// (citit din /etc/os-release de os-release.js), fără să depindă de i18n.
(function () {
  function rebrandTextNodes(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
    var node;
    while ((node = walker.nextNode())) {
      var rebranded = window.OSRelease.rebrand(node.nodeValue);
      if (rebranded !== node.nodeValue) node.nodeValue = rebranded;
    }
  }

  function applyBranding() {
    if (!window.OSRelease) return;
    document.title = window.OSRelease.rebrand(document.title);
    rebrandTextNodes(document.body);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyBranding);
  } else {
    applyBranding();
  }
})();
