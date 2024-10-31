document.getElementById('uploadButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const output = document.getElementById('inputData');

    if (fileInput.files.length === 0) {
        output.textContent = 'Please select a file to upload.';
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const fileContent = e.target.result;
        output.value = fileContent; // Display the content of the file
    };

    reader.onerror = function(e) {
        output.textContent = 'Error reading file: ' + e.target.error;
    };

    reader.readAsText(file); // Read the file as text
});

document.getElementById('uploadButtonE').addEventListener('click', function() {
    const fileInputE = document.getElementById('fileInputE');
    const output = document.getElementById('responseFieldEntities');

    if (fileInputE.files.length === 0) {
        output.textContent = 'Please select a file to upload.';
        return;
    }

    const fileE = fileInputE.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const fileContentE = e.target.result;
        output.textContent = fileContentE; // Display the content of the file
    };

    reader.onerror = function(e) {
        output.textContent = 'Error reading file: ' + e.target.error;
    };

    reader.readAsText(fileE); // Read the file as text
});