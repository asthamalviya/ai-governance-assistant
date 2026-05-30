/**
 * AI Governance & Knowledge Assistant - Frontend Logic
 */

const API_BASE = "http://localhost:8000";

function showResult(elementId, message, isError = false) {
    const el = document.getElementById(elementId);
    el.textContent = message;
    el.classList.add("visible");
    el.classList.toggle("error", isError);
}

// Upload Document
document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData,
        });
        const data = await res.json();
        if (res.ok) {
            showResult("upload-result",
                `Uploaded: ${data.filename}\nDocument ID: ${data.document_id}\nS3 Key: ${data.s3_key}`
            );
        } else {
            showResult("upload-result", `Error: ${data.detail}`, true);
        }
    } catch (err) {
        showResult("upload-result", `Network error: ${err.message}`, true);
    }
});

// Summarise Document
document.getElementById("summarise-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const s3Key = document.getElementById("summarise-key").value;

    try {
        const res = await fetch(`${API_BASE}/summarise`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ document_id: "user-request", s3_key: s3Key }),
        });
        const data = await res.json();
        if (res.ok) {
            showResult("summarise-result", data.summary);
        } else {
            showResult("summarise-result", `Error: ${data.detail}`, true);
        }
    } catch (err) {
        showResult("summarise-result", `Network error: ${err.message}`, true);
    }
});

// Ask Question
document.getElementById("ask-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const s3Key = document.getElementById("ask-key").value;
    const question = document.getElementById("question-input").value;

    try {
        const res = await fetch(`${API_BASE}/ask`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                document_id: "user-request",
                s3_key: s3Key,
                question: question,
            }),
        });
        const data = await res.json();
        if (res.ok) {
            showResult("ask-result", data.answer);
        } else {
            showResult("ask-result", `Error: ${data.detail}`, true);
        }
    } catch (err) {
        showResult("ask-result", `Network error: ${err.message}`, true);
    }
});
