// Preload safety data when the extension is installed
chrome.runtime.onInstalled.addListener(() => {
    const testData = {
        "google.com": { safe: false, alternatives: [{ name: "DuckDuckGo", url: "https://duckduckgo.com" }] },
        "example.com": { safe: false, alternatives: [{ name: "SafeAlternative", url: "https://safealternative.com" }] },
        "facebook.com": { safe: false, alternatives: [{ name: "MeWe", url: "https://mewe.com" }] },
        "www.facebook.com": { safe: false, alternatives: [{ name: "MeWe", url: "https://mewe.com" }] } 
    };
    
    chrome.storage.local.set(testData, () => {
        console.log("Preloaded safety data:", testData);
    });
});

// Listen for messages from content.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'ANALYZE_DOMAIN') {
        console.log("Received domain for analysis:", request.domain);

        // Retrieve preloaded data
        chrome.storage.local.get([request.domain], (data) => {
            if (data[request.domain]) {
                console.log("Using preloaded data for:", request.domain);
                sendResponse(data[request.domain]); // Send the preloaded result
            } else {
                console.log("No preloaded data for:", request.domain);
                sendResponse({ safe: null, alternatives: [] });
            }
        });

        return true; // Keep sendResponse alive for async processing
    }
});
    
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {
        try {
            let domain = new URL(tab.url).hostname;
            chrome.storage.local.get([domain], (data) => {
                if (data[domain] && data[domain].safe === false) {
                    chrome.action.openPopup();
                }
            });
        } catch (error) {
            console.error("Failed to parse URL:", tab.url, error);
        }
    }
});
