## Phishing Detector Browser Extension
A lightweight, real-time phishing detection browser extension for Chrome and Firefox. It warns users about suspicious websites, lookalike domains, and dangerous login forms before they enter their credentials. 

## IT JUST WORKS.

# Features:
- Real-time URL Analysis: Detects typosquatting and lookalike domains (examples -- paypa1.com, g00gle.com)
- Form Protection: Scans login forms and alerts if they submit to suspicious endpoints
- Domain Similarity Check: Uses Levenshtein distance algorithm for smart detection
- Entropy Analysis: Flags randomly generated phishing domains
- Browser Notifications: Clear alerts when threats are detected
- Options Page: Enable/disable protection easily
- Works on All Sites

## How It Works
The extension uses the WebExtensions API to:
- Monitor navigation events
- Analyze page URLs and form actions
- Apply multiple detection techniques (string similarity + entropy)
- Show instant warnings via alerts and notifications

## Tech Stack
- JavaScript (Manifest V3)
- Chrome WebExtensions API
- Levenshtein Distance Algorithm
- MutationObserver for dynamic content

## Installation 
- Clone or download this repository
- Open Chrome and go to chrome://extensions/
- Enable Developer mode (top right)
- Load unpacked and select the project folder
- The extension is now active!

