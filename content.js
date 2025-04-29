function extractEmailContent() {
  // Gmail uses dynamic elements — look inside the 'div[role="main"]' or 'div[dir="ltr"]'
  const emailBody = document.querySelector('div[dir="ltr"]');
  if (emailBody) {
    return emailBody.innerText;
  }
  return null;
}

function checkEmail() {
  const content = extractEmailContent();
  if (content) {
    fetch("https://email-j0oc.onrender.com/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: content }) // You may want to rename this later
    })
    
    .then(res => res.json())
    .then(data => {
      alert(`Email is: ${data.prediction}`); // or inject a tooltip like Grammarly
    })
    .catch(err => console.error(err));
  }
}

// Gmail is a SPA, so we use MutationObserver to detect view changes
const observer = new MutationObserver(() => {
  setTimeout(checkEmail, 2000); // slight delay for content to load
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});

function showTooltip(result) {
  let tooltip = document.createElement("div");
  tooltip.style.position = "fixed";
  tooltip.style.bottom = "20px";
  tooltip.style.right = "20px";
  tooltip.style.background = result === "Legitimate" ? "#4CAF50" : "#F44336";
  tooltip.style.color = "#fff";
  tooltip.style.padding = "10px 20px";
  tooltip.style.borderRadius = "10px";
  tooltip.style.boxShadow = "0 0 10px rgba(0,0,0,0.2)";
  tooltip.style.zIndex = 9999;
  tooltip.innerText = `Email is: ${result}`;
  document.body.appendChild(tooltip);
  setTimeout(() => tooltip.remove(), 5000); // auto remove
}