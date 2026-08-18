function open_gparted() {
const { exec } = require('child_process');
exec('gparted', (err, stdout, stderr) => {
    if (err) {
        console.error('Error opening GParted:', err.message);
        alert('GParted could not be opened. Make sure it is installed.');
        return;
    }
    // GParted opened successfully
})
}

function open_browser() {
const { exec } = require('child_process');
// Try Pafari first, fallback to xdg-open or firefox
exec('pafari', (err) => {
    if (err) {
        // Pafari not found, try xdg-open
        exec('xdg-open http://www.google.com', (err2) => {
            if (err2) {
                // xdg-open failed, try firefox
                exec('firefox', (err3) => {
                    if (err3) {
                        console.error('Error opening browser:', err3.message);
                        alert('Could not open browser. Make sure a browser is installed.');
                    }
                });
            }
        });
    }
});
}

function open_packup() {
const { exec } = require('child_process');
// TODO: Implement packup restore functionality
// For now, just show a message or open packup application if available
exec('packup &', (err) => {
    if (err) {
        console.error('Packup not available:', err.message);
        alert('Packup restore functionality is not yet implemented or Packup is not installed.');
    }
})
}

function open_installer() {
  const { spawn } = require('child_process');
  const child = spawn('sudo', ['/usr/bin/calamares-install-debian'], {
    detached: true,
    stdio: 'ignore',
    env: Object.assign({}, process.env)
  });
  child.unref();
}

// Menu checkbox functionality
function initMenuCheckboxes() {
  var checkboxes = document.querySelectorAll('.menu_checkbox');

  // Update visual state for all checkboxes on init
  checkboxes.forEach(function(checkbox) {
    updateMenuCheckboxState(checkbox);
  });

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
      // If this checkbox is checked, uncheck all others
      if (this.checked) {
        checkboxes.forEach(function(cb) {
          if (cb !== this) {
            cb.checked = false;
            updateMenuCheckboxState(cb);
          }
        }.bind(this));
      }
      // Update visual state
      updateMenuCheckboxState(this);
    });
  });
}

function updateMenuCheckboxState(checkbox) {
  var label = checkbox.closest('.menu_checkbox_label');
  if (checkbox.checked) {
    label.classList.add('menu_checkbox_checked');
  } else {
    label.classList.remove('menu_checkbox_checked');
  }
}

function handleMenuAction(action) {
  // Uncheck all checkboxes first
  var allCheckboxes = document.querySelectorAll('.menu_checkbox');
  allCheckboxes.forEach(function(cb) {
    cb.checked = false;
    updateMenuCheckboxState(cb);
  });
  
  // Check the selected checkbox
  var checkbox = document.getElementById('menu_' + action);
  if (checkbox) {
    checkbox.checked = true;
    updateMenuCheckboxState(checkbox);
  }
  
  // Execute the action
  switch(action) {
    case 'packup':
      open_packup();
      break;
    case 'installer':
      open_installer();
      break;
    case 'browser':
      open_browser();
      break;
    case 'gparted':
      open_gparted();
      break;
  }
}

function handleMenuContinue() {
  var checkedCheckbox = document.querySelector('.menu_checkbox:checked');
  if (!checkedCheckbox) {
    alert('Please select an option');
    return;
  }
  
  // Execute action for the selected item
  var action = checkedCheckbox.value;
  switch(action) {
    case 'packup':
      open_packup();
      break;
    case 'installer':
      var contBtn = document.getElementById('menu-continue-btn');
      if (contBtn) {
        contBtn.disabled = true;
        contBtn.classList.add('disabled');
        setTimeout(function() {
          contBtn.disabled = false;
          contBtn.classList.remove('disabled');
        }, 10000);
      }
      open_installer();
      break;
    case 'browser':
      open_browser();
      break;
    case 'gparted':
      open_gparted();
      break;
  }
}
///////////////////////////////////////////////////////////////////////////////////////////////////
// Mark selected option when language is selected
function markSelectedLanguage() {
  var select = document.getElementById("ddlViewBy");
  if (select) {
    // Remove selected class from all options
    var options = select.getElementsByTagName('option');
    for (var i = 0; i < options.length; i++) {
      options[i].classList.remove('selected-option');
    }
    // Add selected class to current option
    if (select.selectedIndex >= 0) {
      options[select.selectedIndex].classList.add('selected-option');
    }
  }
}

// Initialize on page load
window.addEventListener('load', function() {
  var select = document.getElementById("ddlViewBy");
  if (select) {
    // Mark initial selection
    markSelectedLanguage();
    // Mark selection when changed
    select.addEventListener('change', markSelectedLanguage);
    // Mark selection when focus is lost
    select.addEventListener('blur', markSelectedLanguage);
  }
});

// Initialize language selection handler
function initLanguageSelection() {
  var selectElement = document.getElementById("ddlViewBy");
  if (selectElement) {
    selectElement.addEventListener('change', function() {
      // Remove selected attribute from all options
      for (var i = 0; i < this.options.length; i++) {
        this.options[i].removeAttribute('selected');
      }
      // Set selected attribute on the currently selected option
      if (this.selectedIndex >= 0) {
        this.options[this.selectedIndex].setAttribute('selected', 'selected');
      }
    });
  }
}

function select_language() {
  var e = document.getElementById("ddlViewBy");
  var strUser = e.options[e.selectedIndex].text;
  if (strUser == "English") {
    window.location.href='lg/en/page_examining.html';
  } else if (strUser == "Romanian") {
      window.location.href='lg/ro/page_examining.html';
    }
    else if (strUser == "Czech") {
      window.location.href='lg/cs/page_examining.html';
    }
}
