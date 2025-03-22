// popup.js
document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, async (tabs) => {
        if (!tabs.length) return;  // Prevent errors if no tab is found

        const currentURL = new URL(tabs[0].url);
        const currentDomain = currentURL.hostname;

        const resultEl = document.getElementById('result');
        const alternativesEl = document.getElementById('alternatives');

        resultEl.textContent = "Analyzing website safety...";

        try {
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ domain: currentDomain })
            });

            const data = await response.json();

            if (data.status === 'success') {
                if (data.is_safe) {
                    resultEl.innerHTML = `
                        <div class="safe">
                            <h2>✅ Website is Safe</h2>
                            <p>Privacy policy analysis indicates this site is safe to use.</p>
                            <p><a href="${data.privacy_url}" target="_blank">View Privacy Policy</a></p>
                        </div>
                    `;
                } else {
                    resultEl.innerHTML = `
                        <div class="unsafe">
                            <h2>⚠️ Privacy Concerns Detected</h2>
                            <p>${data.policy_analysis[0]}</p>
                            <details>
                                <summary>See Details</summary>
                                <p>${data.policy_analysis[1]}</p>
                            </details>
                        </div>
                    `;

                    if (data.alternatives) {
                        alternativesEl.innerHTML = '<h3>Alternative Sites:</h3>';
                        for (const [name, url] of Object.entries(data.alternatives)) {
                            const div = document.createElement('div');
                            div.innerHTML = `<a href="${url}" target="_blank">${name}</a>`;
                            alternativesEl.appendChild(div);
                        }
                    }
                }

                // Store the result in chrome.storage.local
                chrome.storage.local.set({
                    [currentDomain]: {
                        safe: data.is_safe,
                        alternatives: data.alternatives ? Object.entries(data.alternatives).map(([name, url]) => ({ name, url })) : []
                    }
                });

            } else {
                resultEl.textContent = `Error: ${data.message}`;
            }
        } catch (error) {
            resultEl.textContent = `Error: ${error.message}`;
        }
    });
});
