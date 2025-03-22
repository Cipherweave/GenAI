chrome.storage.local.get([currentDomain], data => {
    const result = data[currentDomain];
    const resultEl = document.getElementById('result');
    
    if (result.safe) {
      resultEl.textContent = "✅ This site is safe";
    } else {
      resultEl.textContent = "⚠️ Potential risks detected";
      result.alternatives.forEach(site => {
        const div = document.createElement('div');
        div.innerHTML = `<a href="${site.url}">${site.name}</a>`;
        document.getElementById('alternatives').appendChild(div);
      });
    }
  });
  