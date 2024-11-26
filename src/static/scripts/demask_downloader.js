document.getElementById('downloadBtnDemask').addEventListener('click', function() {

    const contents = [
        { content: document.getElementById('responseFieldDeanonText').value, name: 'yoyo-text.txt', type: 'text/plain' },
    ];
    
    // Download files
    async function downloadFiles(files) {
        for (const file of files) {
            const blob = new Blob([file.content], { type: file.type });
            const url = window.URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = file.name;
            document.body.appendChild(a);
            a.click();
            a.remove();
            
            window.URL.revokeObjectURL(url);

            await new Promise(resolve => setTimeout(resolve, 100));
        };
    }
    
    downloadFiles(contents);
});