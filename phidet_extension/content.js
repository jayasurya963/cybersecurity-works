// Levenshtein distance for better typosquatting detection
function levenshtein(a, b) {
  const matrix = [];
  for (let i = 0; i <= b.length; i++) matrix[i] = [i];
  for (let j = 0; j <= a.length; j++) matrix[0][j] = j;

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      if (a[i-1] === b[j-1]) {
        matrix[i][j] = matrix[i-1][j-1];
      } else {
        matrix[i][j] = Math.min(
          matrix[i-1][j-1] + 1,
          matrix[i][j-1] + 1,
          matrix[i-1][j] + 1
        );
      }
    }
  }
  return matrix[a.length][b.length];
}


// content.js
function isSuspiciousUrl(url) {
  try {
    const hostname = new URL(url).hostname.toLowerCase().replace('www.', '');
    
    const legitDomains = [
      'paypal.com', 'google.com', 'facebook.com', 'microsoft.com',
      'apple.com', 'amazon.com', 'bankofamerica.com', 'chase.com'
    ];

    for (let legit of legitDomains) {
      const legitHost = legit.replace('www.', '');
      const distance = levenshtein(hostname, legitHost);
      
      // Flag if very similar but not exact
      if (distance > 0 && distance <= 3 && 
          Math.max(hostname.length, legitHost.length) <= 25) {
        return true;
      }
    }

    // Entropy check for gibberish domains
    if (calculateEntropy(hostname) > 4.2) {
      return true;
    }

    // Keyword + TLD suspicion
    if (/(\.ru|\.cn|\.top|\.xyz|\.tk|\.ml|login|secure|account|update|support|verify)/.test(hostname)) {
      return true;
    }

    return false;
  } catch (e) {
    return false;
  }
}

// Entropy helper (high entropy = random-looking = suspicious)
function calculateEntropy(str) {
  const freq = {};
  for (let char of str) freq[char] = (freq[char] || 0) + 1;
  let entropy = 0;
  for (let char in freq) {
    const p = freq[char] / str.length;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}
function checkForms() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    const action = form.getAttribute('action') || window.location.href;
    if (isSuspiciousUrl(action)) {
      alert("⚠️ Potential phishing form detected! Do not enter credentials.");
      chrome.runtime.sendMessage({ 
        type: "PHISHING_ALERT", 
        url: action 
      });
    }
  });
}

// Run initial checks safely
function runChecks() {
  if (isSuspiciousUrl(window.location.href)) {
    chrome.runtime.sendMessage({ 
      type: "PHISHING_ALERT", 
      url: window.location.href 
    });
  }
  checkForms();
}

// Wait for DOM to be ready
if (document.readyState === "loading") {
  document.addEventListener('DOMContentLoaded', runChecks);
} else {
  runChecks();
}

// MutationObserver for dynamically added forms
const observer = new MutationObserver(() => {
  checkForms();
});

if (document.body) {
  observer.observe(document.body, { childList: true, subtree: true });
} else {
  document.addEventListener('DOMContentLoaded', () => {
    observer.observe(document.body, { childList: true, subtree: true });
  });
}