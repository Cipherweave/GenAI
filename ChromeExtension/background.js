// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'UPDATE_ICON') {
      // Change icon based on site safety using only 48px icons
      chrome.action.setIcon({
        path: message.isSafe ? "icons/lock-solid.svg" : "icons/lock-open-solid.svg"
      });
      
      // Optionally set badge
      chrome.action.setBadgeText({
        text: message.isSafe ? "✓" : "!"
      });
      
      chrome.action.setBadgeBackgroundColor({
        color: message.isSafe ? "#2ecc71" : "#e74c3c"
      });
    }
    
    // Rest of your message handling code...
  });
  
  // When checking cached data in tabs.onUpdated
  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {
      try {
        let domain = new URL(tab.url).hostname;
        chrome.storage.local.get([domain], (data) => {
          if (data[domain]) {
            // Update icon based on stored safety data - simplified to just 48px
            chrome.action.setIcon({
              tabId: tabId,
              path: data[domain].safe ? "icons/lock-solid.svg" : "icons/lock-open-solid.svg"
            });
            
            // If site is unsafe, open popup
            if (data[domain].safe === false) {
              chrome.action.openPopup();
            }
          } else {
            // Reset to default icon when no data is available
            chrome.action.setIcon({
              tabId: tabId,
              path: "icons/lock-open-solid.svg"
            });
          }
        });
      } catch (error) {
        console.error("Failed to parse URL:", tab.url, error);
      }
    }
  });
  