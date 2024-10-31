document.getElementById('downloadBtnDemask').addEventListener('click', function() {
    // Get the content of the textarea
    const Text = document.getElementById('responseFieldDeanonText').value;

    // Create a Blob from the textarea content
    const blobText = new Blob([Text], { type: 'text/plain' });

    // Create a link element
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blobText);
    link.download = 'yoyo-text.txt'; // Specify the file name

    // Programmatically click the link to trigger the download
    link.click();

    // Clean up and revoke the object URL
    URL.revokeObjectURL(link.href);
});