
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getEmailText') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs[0];
      chrome.scripting.executeScript(
        {
          target: { tabId: tab.id },
          func: extractEmailContent
        },
        (injectionResults) => {
          const emailText = injectionResults[0].result;
          sendResponse({ emailText: emailText });
        }
      );
    });
    return true;
  }
});

function extractEmailContent() {
  const emailBody = document.body.innerText;
  return emailBody;
}
