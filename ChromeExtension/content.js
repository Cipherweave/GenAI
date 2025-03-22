// Get current domain and send to background
const currentDomain = new URL(window.location.href).hostname;

chrome.runtime.sendMessage({
  type: 'ANALYZE_DOMAIN',
  domain: currentDomain
});
