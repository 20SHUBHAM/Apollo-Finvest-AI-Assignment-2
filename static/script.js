document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('callForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const borrowerName = document.getElementById('borrowerName').value;
        const borrowerPhone = document.getElementById('borrowerPhone').value;
        const language = document.getElementById('language').value;

        fetch('/call/initiate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name: borrowerName, phone: borrowerPhone, language: language })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data);
        })
        .catch(err => {
            document.getElementById('response').innerText = "Error initiating call.";
            console.error(err);
        });
    });
});
