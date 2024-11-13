document.getElementById('downloadBtn').addEventListener('click', function() {
    // Get the content of the textarea
    const foundEntities = document.getElementById('responseFieldEntities').value;
    const newText = document.getElementById('responseFieldAnonText').value;

    // Create a Blob from the textarea content
    const blobEntities = new Blob([foundEntities], { type: 'application/json' });
    const blobNewText = new Blob([newText], { type: 'text/plain' });

    // Create a link element
    const linkE = document.createElement('a');
    linkE.href = URL.createObjectURL(blobEntities);
    linkE.download = 'yoyo-entities.json'; // Specify the file name

    const linkNT = document.createElement('a');
    linkNT.href = URL.createObjectURL(blobNewText);
    linkNT.download = 'yoyo-anonymizedText.txt'; // Specify the file name
    
    linkE.click();
    URL.revokeObjectURL(linkE.href);

    setTimeout(function() {
        linkNT.click();
        URL.revokeObjectURL(linkNT.href)
    }, 50);
});