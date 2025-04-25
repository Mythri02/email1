// content.js
const targetNode = document.body;
const config = { childList: true, subtree: true };

let lastEmailText = "";

const callback = function(mutationsList, observer) {
    let emailBody = document.querySelector('div[role="listitem"] div[dir="ltr"]');
    if (emailBody) {
        const text = emailBody.innerText;
        if (text && text !== lastEmailText) {
            lastEmailText = text; // Update last seen email
            chrome.runtime.sendMessage({ emailText: text });
        }
    }
};

const observer = new MutationObserver(callback);
observer.observe(targetNode, config);
