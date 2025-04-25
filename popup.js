// Listen for the click event on the "Analyze Email" button
document.getElementById('analyzeButton').addEventListener('click', function() {
  const emailLink = document.getElementById('emailLink').value;  // Get the input URL

  if (emailLink) {
      // Send the email link to the background script for analysis
      chrome.runtime.sendMessage({ action: 'analyze', link: emailLink }, function(response) {
          // Handle the response here
          alert(`Analysis Result: ${response.result}`);
      });
  } else {
      alert("Please paste a link to analyze.");
  }
});
