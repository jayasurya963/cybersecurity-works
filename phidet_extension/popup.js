document.getElementById('status').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url = tabs[0].url;
  
      alert(
        isSuspiciousUrl(url)
          ? "⚠️ This page looks suspicious!"
          : "✅ Looks safe."
      );
    });
  });
  
  function isSuspiciousUrl(url) {
    try {
      const hostname = new URL(url).hostname.toLowerCase();
  
      const legitDomains = [
        "paypal.com",
        "google.com",
        "facebook.com",
        "microsoft.com"
      ];
  
      const suspiciousPatterns = [
        /paypa1\.com/i,
        /g00gle\.com/i,
        /faceb00k\.com/i
      ];
  
      if (suspiciousPatterns.some(pattern => pattern.test(hostname))) {
        return true;
      }
  
      return legitDomains.some(legit => {
        const legitName = legit.replace(".com", "");
  
        return (
          hostname.includes(legitName) &&
          hostname !== legit
        );
      });
  
    } catch {
      return false;
    }
  }