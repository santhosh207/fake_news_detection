chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: extractText
  });
});

function extractText() {
  const text = document.documentElement.innerText;
  chrome.runtime.sendMessage({ action: "textExtracted", text: text });
}
