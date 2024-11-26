document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    document.getElementById('loading-spinner').style.display = 'flex'; // Show the loading spinner

    const inputData = document.getElementById('inputData').value;
    const inputDataEntities = JSON.parse(document.getElementById('responseFieldEntities').value);

    const apiEndpoint = '/api/demask'; // Set API endpoint

    // Send a POST request to the API
    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputData, entities: inputDataEntities}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(text => {
        // Display the response in the textarea
        document.getElementById('responseFieldText').value = inputData;
        document.getElementById('responseFieldDeanonText').value = text.deanonymized_text;

        document.getElementById('loading-spinner').style.display = 'none'; // Hide the loading spinner
        
    })
    .catch((error) => {
        console.error('Error:', error); // Handle any errors
        // Optionally display the error in the textarea
        document.getElementById('responseFieldDeanonText').value = 'Error: ' + error.message + '\nEntities: ' + inputDataEntities + '\nText: ' + inputData;
    });
});