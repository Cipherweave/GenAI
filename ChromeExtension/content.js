const currentDomain = new URL(window.location.href).hostname;

chrome.runtime.sendMessage({ type: 'ANALYZE_DOMAIN', domain: currentDomain }, (response) => {
    if (response && response.safe === false) {
        const warningBanner = document.createElement('div');
        warningBanner.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: red;
                color: white;
                text-align: center;
                padding: 10px;
                font-size: 16px;
                z-index: 9999;">
                ⚠️ Warning: This site may not be safe! 
                <br> Consider alternatives:
            </div>
        `;

        document.body.prepend(warningBanner);
    }
});
