// content_script.js
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "extractText") {
    const text = document.documentElement.innerText;
    sendResponse({ text: text });
  }
});
