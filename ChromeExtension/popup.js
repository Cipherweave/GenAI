// popup.js
document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, async (tabs) => {
        if (!tabs.length) return;  // Prevent errors if no tab is found

        const currentURL = new URL(tabs[0].url);
        const currentDomain = currentURL.hostname;

        const loadingEl = document.getElementById('loading');
        const resultEl = document.getElementById('result');
        const alternativesEl = document.getElementById('alternatives');
        const alternativesList = document.querySelector('.alternatives-list');

        try {
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ domain: currentDomain })
            });

            const data = await response.json();
            
            // Hide loading spinner
            loadingEl.style.display = 'none';

            if (data.status === 'success') {
                if (data.is_safe) {
                    resultEl.innerHTML = `
                        <div class="safe">
                            <h2><i class="fas fa-check-circle" style="color: var(--success-color)"></i> Website is Safe</h2>
                            <p>Privacy policy analysis indicates this site is safe to use.</p>
                            <p><a href="${data.privacy_url}" target="_blank">View Privacy Policy <i class="fas fa-external-link-alt"></i></a></p>
                        </div>
                    `;
                    alternativesEl.style.display = 'none';
                } else {
                    resultEl.innerHTML = `
                        <div class="unsafe">
                            <h2><i class="fas fa-exclamation-triangle" style="color: var(--warning-color)"></i> Privacy Concerns Detected</h2>
                            <p>${data.policy_analysis[0]}</p>
                            <details>
                                <summary>See Details</summary>
                                <p>${data.policy_analysis[1]}</p>
                            </details>
                        </div>
                    `;

                    if (data.alternatives && Object.keys(data.alternatives).length > 0) {
                        alternativesList.innerHTML = '';
                        
                        for (const [name, url] of Object.entries(data.alternatives)) {
                            const link = document.createElement('a');
                            link.href = url;
                            link.target = '_blank';
                            link.textContent = name;
                            alternativesList.appendChild(link);
                        }
                        
                        alternativesEl.style.display = 'block';
                    } else {
                        alternativesEl.style.display = 'none';
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
                resultEl.innerHTML = `
                    <div class="unsafe">
                        <h2><i class="fas fa-times-circle" style="color: var(--warning-color)"></i> Error</h2>
                        <p>${data.message}</p>
                    </div>
                `;
                alternativesEl.style.display = 'none';
            }
        } catch (error) {
            loadingEl.style.display = 'none';
            resultEl.innerHTML = `
                <div class="unsafe">
                    <h2><i class="fas fa-times-circle" style="color: var(--warning-color)"></i> Error</h2>
                    <p>${error.message}</p>
                </div>
            `;
            alternativesEl.style.display = 'none';
        }
    });
});
