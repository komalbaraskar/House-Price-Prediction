document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const resultBox = document.createElement('div');
  resultBox.className = 'result-box';
  form.appendChild(resultBox);

  // Chart setup
  const ctx = document.getElementById('priceChart').getContext('2d');
  const chartData = {
    labels: [],
    datasets: [{
      label: 'Predicted Price History',
      data: [],
      borderColor: '#4CAF50',
      borderWidth: 2,
      fill: false
    }]
  };
  const chart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } }
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const sqft = document.getElementById('sqft').value;
    const bedrooms = document.getElementById('bedrooms').value;
    const bathrooms = document.getElementById('bathrooms').value;
    const zipcode = document.getElementById('zipcode').value;
    const year_built = document.getElementById('year_built').value;

    const inputData = {
      sqft: parseFloat(sqft),
      bedrooms: parseFloat(bedrooms),
      bathrooms: parseFloat(bathrooms),
      zipcode: parseInt(zipcode),
      year_built: parseInt(year_built)
    };

    try {
      const response = await fetch('/api/predict/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inputData)
      });

      const data = await response.json();

      if (data.predicted_price) {
        resultBox.innerHTML = `<h3>🏡 Predicted Price: <span>$${data.predicted_price.toLocaleString()}</span></h3>`;

        // Update chart
        chart.data.labels.push(new Date().toLocaleTimeString());
        chart.data.datasets[0].data.push(data.predicted_price);
        chart.update();
      } else {
        resultBox.innerHTML = `<p style="color:red;">⚠️ ${data.error || 'Prediction failed.'}</p>`;
      }
    } catch (error) {
      console.error('Error:', error);
      resultBox.innerHTML = `<p style="color:red;">❌ Could not connect to API.</p>`;
    }
  });
});
