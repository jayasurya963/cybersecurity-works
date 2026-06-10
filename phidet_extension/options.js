document.getElementById('save').addEventListener('click', () => {
    const enabled = document.getElementById('enabled').checked;
    chrome.storage.sync.set({ enabled: enabled }, () => {
      alert("Settings saved!");
    });
  });
  
  // Load current settings
  chrome.storage.sync.get('enabled', (data) => {
    document.getElementById('enabled').checked = data.enabled !== false;
  });