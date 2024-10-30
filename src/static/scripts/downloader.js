document.getElementById('downloadBtn').addEventListener('click', function() {
    // Get the content of the textarea
    const foundEntities = document.getElementById('responseFieldEntities').value;

    // Create a Blob from the textarea content
    const blob = new Blob([foundEntities], { type: 'application/json' });

    // Create a link element
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'yoyo-entities.json'; // Specify the file name

    // Programmatically click the link to trigger the download
    link.click();

    // Clean up and revoke the object URL
    URL.revokeObjectURL(link.href);
});
