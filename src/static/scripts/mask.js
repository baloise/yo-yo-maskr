// shows/hides checkbox when LLM is selected
document.getElementById('backendType').addEventListener('change', function() {
    var llmInputCheckbox = document.getElementById('LLMcustomLabel');
    if (this.value === 'LLM') {
        llmInputCheckbox.style.display = 'flex';
    } else {
        var llmInputDiv = document.getElementById('LLMInput');
        var llmInputReset = document.getElementById('LLMReset');
        llmInputCheckbox.style.display = 'none'; // Hide the LLMcustomLabel div
        llmInputDiv.style.display = 'none'; // Hide the LLMInput div
        llmInputReset.style.display = 'none'; // Hide the LLMReset div
    }
});

// shows/hides custom input fields when checkbox is checked
document.getElementById('LLMcustom').addEventListener('change', function() {
    var llmInputDiv = document.getElementById('LLMInput');
    var llmInputReset = document.getElementById('LLMReset');
    if (this.checked === true) {
        llmInputDiv.style.display = 'flex'; // Show the LLMInput div
        llmInputReset.style.display = 'flex'; // Show the LLMReset div
    } else {
        llmInputDiv.style.display = 'none'; // Hide the LLMInput div
        llmInputReset.style.display = 'none'; // Hide the LLMReset div
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

    document.getElementById('loading-spinner').style.display = 'flex'; // Show the loading spinner
    const inputData = document.getElementById('inputData').value;
    const backendType = document.getElementById('backendType').value;
    const inputLLMurl = document.getElementById('inputLLMurl').value;
    const inputLLMmodel = document.getElementById('inputLLMmodel').value;
    
    const apiEndpoint = '/api/mask'; // Set API endpoint

    // Send a POST request to the API
    fetch(apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputData, "backendType": backendType, llmURL: inputLLMurl, llmModel: inputLLMmodel}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(text => {

        // Display the response in the textarea, no JSON formatting for text
        document.getElementById('responseFieldText').value = text.original_text;
        document.getElementById('responseFieldEntities').value = JSON.stringify(text.entities, null, 2);
        document.getElementById('responseFieldAnonText').value = text.anonymized_text;

        document.getElementById('loading-spinner').style.display = 'none'; // Hide the loading spinner
    })
    .catch((error) => {
        console.error('Error:', error); // Handle any errors
        document.getElementById('responseFieldText').value = 'Error: ' + error.message + '\nText: ' + inputData; // display the error in the textarea
    });
});