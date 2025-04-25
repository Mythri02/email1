function analyzeEmail(text) {
  fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email: text })
  })
  .then(response => response.json())
  .then(data => {
      const result = document.getElementById("result");
      if (data.result === 'Phishing') {
          result.innerText = "⚠️ This email might be a phishing attempt!";
      } else {
          result.innerText = "✅ This email looks legitimate.";
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
