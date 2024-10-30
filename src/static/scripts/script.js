document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const inputData = document.getElementById('inputData').value;

    // Use a relative URL for the API endpoint
    const apiEndpoint = '/api/mask'; // Relative URL

    // Send a POST request to the API
    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputData }), // Send the input text as JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(text => {
        // Display the response in the textarea
        document.getElementById('responseField').value = JSON.stringify(text, null, 2); // Format the JSON response
    })
    .catch((error) => {
        console.error('Error:', error); // Handle any errors
        // Optionally display the error in the textarea
        document.getElementById('responseField').value = 'Error: ' + error.message;
    });
});