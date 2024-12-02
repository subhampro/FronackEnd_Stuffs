document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        document.getElementById('result').innerHTML = result.success 
            ? `<p style="color: green;">Conversion successful! <a href="${result.downloadUrl}">Download DDS</a></p>`
            : `<p style="color: red;">Error: ${result.error}</p>`;
    } catch (error) {
        document.getElementById('result').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});