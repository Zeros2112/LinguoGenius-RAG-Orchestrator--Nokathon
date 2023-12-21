// app.js
async function uploadDocument() {
    const form = document.getElementById("uploadForm");
    const formData = new FormData(form);

    try {
        const response = await fetch("/upload_document", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.success) {
            // Document uploaded successfully, show the question form
            document.getElementById("uploadForm").style.display = "none";
            document.getElementById("questionForm").style.display = "block";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("response").innerText = "An error occurred while uploading the document.";
    }
}

// app.js
async function generateResponse() {
    const question = document.getElementById("question").value;
    const formData = new FormData();
    formData.append("question", question);

    try {
        const response = await fetch("/generate_response", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.text();
        document.getElementById("response").innerHTML = data; // Use innerHTML to render HTML content
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("response").innerText = "An error occurred.";
    }
}
