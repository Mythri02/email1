// Listen for messages from the popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'analyze') {
      const link = message.link;

      // Call your phishing detection logic here
      // For now, we are just simulating with a placeholder
      let result = 'Safe'; // Default result

      // Example simple check (You can replace this with a more advanced method or API call)
      if (link.includes('phishing')) {
          result = 'Phishing detected!';
      }

      // Send back the result to the popup
      sendResponse({ result: result });
  }
});
