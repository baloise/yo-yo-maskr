// shows/hides checkbox when LLM is selected
document.getElementById('backendType').addEventListener('change', function() {
    var llmInputCheckbox = document.getElementById('LLMcustomLabel');
    if (this.value === 'LLM') {
        llmInputCheckbox.style.display = 'flex';
    } else {
        llmInputCheckbox.style.display = 'none';
    }
});

// shows/hides custom input fields when checkbox is checked
document.getElementById('LLMcustom').addEventListener('change', function() {
    var llmInputDiv = document.getElementById('LLMInput');
    var llmInputReset = document.getElementById('LLMReset');
    if (this.checked === true) {
        llmInputDiv.style.display = 'flex'; // Show the LLMInput div
        llmInputReset.style.display = 'flex';
    } else {
        llmInputDiv.style.display = 'none'; // Hide the LLMInput div
        llmInputReset.style.display = 'none';
    }
});

// Load values from local storage when checkbox is true
document.getElementById('LLMcustom').addEventListener('change', function() {
    const llmUrl = localStorage.getItem('LLMURL');
    const llmModel = localStorage.getItem('LLMMODEL');

    if (this.checked === true) {
        if (llmUrl) {
            document.getElementById('inputLLMurl').value = llmUrl;
        }
        if (llmModel) {
            document.getElementById('inputLLMmodel').value = llmModel;
        }
    } else {
        document.getElementById('inputLLMurl').value = "";
        document.getElementById('inputLLMmodel').value = "";
    }
});

// Store values in local storage when form is submitted
document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Get the values from the input fields
    const llmUrl = document.getElementById('inputLLMurl').value;
    const llmModel = document.getElementById('inputLLMmodel').value;

    // Store the values in local storage if value is set
    if (llmUrl) {
        localStorage.setItem('LLMURL', llmUrl);
    }
    if (llmModel) {
        localStorage.setItem('LLMMODEL', llmModel);
    }
});

// Reset stored values when reset button is clicked
document.getElementById('btnLLMReset').addEventListener('click', function() {
    alert('Reset stored custom LLM settings');
    document.getElementById('inputLLMurl').value = "";
    localStorage.setItem('LLMURL', "");

    document.getElementById('inputLLMmodel').value = "";
    localStorage.setItem('LLMMODEL', "");
});

document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const inputData = document.getElementById('inputData').value;
    const backendType = document.getElementById('backendType').value;
    const inputLLMurl = document.getElementById('inputLLMurl').value;
    const inputLLMmodel = document.getElementById('inputLLMmodel').value;
    
    // Use a relative URL for the API endpoint
    const apiEndpoint = '/api/mask'; // Relative URL

    // Send a POST request to the API
    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputData, "backendType": backendType, llmURL: inputLLMurl, llmModel: inputLLMmodel}), // Send the input text as JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response
    })
    .then(text => {
        // Display the response in the textarea
        document.getElementById('responseFieldText').value = JSON.stringify(text.original_text, null, 2); // Format the JSON response
        document.getElementById('responseFieldEntities').value = JSON.stringify(text.entities, null, 2); // Format the JSON response
        document.getElementById('responseFieldAnonText').value = JSON.stringify(text.anonymized_text, null, 2); // Format the string response
    })
    .catch((error) => {
        console.error('Error:', error); // Handle any errors
        // Optionally display the error in the textarea
        document.getElementById('responseFieldText').value = 'Error: ' + error.message + '\nText: ' + inputData;
    });
});