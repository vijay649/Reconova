// // ==========================================
// // SAFED ELEMENT COUNTER CHANGE HANDLER
// // ==========================================
// function updateFolderStatus() {
//     const input = document.getElementById("folderInput");
//     const display = document.getElementById("fileCountDisplay");
//     const status = document.getElementById("status");
    
//     if (input && input.files) {
//         let count = 0;
//         for (const file of input.files) {
//             if (file.name.toLowerCase().endsWith(".pdf")) {
//                 count++;
//             }
//         }
        
//         // HTML Dropzone text ko update karein
//         if (display) {
//             display.innerText = `Selected: ${count} documents queued`;
//             display.style.color = '#16a34a';
//         }
        
//         // Niche ke status container ko reset karein
//         if (status) {
//             status.innerText = `📁 ${count} PDF files detected in folder. Ready to parse!`;
//             status.style.color = "#4b5563";
//         }
//     }
// }

// // Global scope window clean bindings
// window.updateFolderStatus = updateFolderStatus;

// async function uploadFolder() {
//     const input = document.getElementById("folderInput");
//     const sourceSelect = document.getElementById("sourceSelect");
//     const status = document.getElementById("status");
//     const runBtn = document.getElementById("runParserBtn");

//     if (!input || !sourceSelect || !status || !runBtn) {
//         alert("Frontend layout element rendering error.");
//         return;
//     }

//     const files = input.files;

//     // =====================================
//     // FILE VALIDATION
//     // =====================================
//     if (!files || !files.length) {
//         status.innerText = "⚠️ Please select folder first";
//         status.style.color = "red";
//         return;
//     }

//     const formData = new FormData();
//     let pdfCount = 0;

//     for (const file of files) {
//         if (file.name.toLowerCase().endsWith(".pdf")) {
//             formData.append("files", file);
//             pdfCount++;
//         }
//     }

//     if (pdfCount === 0) {
//         status.innerText = "⚠️ No PDF files found";
//         status.style.color = "red";
//         return;
//     }

//     // =====================================
//     // TOKEN
//     // =====================================
//     const token = localStorage.getItem("token");

//     if (!token) {
//         alert("Session expired. Login again");
//         window.location.href = "../pages/login.html";
//         return;
//     }

//     // =====================================
//     // API
//     // =====================================
//     const source = sourceSelect.value;
//     const endpoint = `${API_BASE_URL}/${source}`;

//     runBtn.disabled = true;

//     try {
//         status.innerText = `⏳ Processing ${pdfCount} PDF files...`;
//         status.style.color = "#2563eb";

//         const response = await fetch(endpoint, {
//             method: "POST",
//             headers: {
//                 "Authorization": `Bearer ${token}`
//             },
//             body: formData
//         });

//         console.log("Response Status:", response.status);

//         // =====================================
//         // ERROR RESPONSE
//         // =====================================
//         if (!response.ok) {
//             let message = "Excel generation failed";
//             try {
//                 const error = await response.json();
//                 message = error.detail || message;
//             } catch (e) {}
//             throw new Error(message);
//         }

//         // =====================================
//         // RECEIVE EXCEL
//         // =====================================
//         const blob = await response.blob();

//         if (blob.size <= 0) {
//             throw new Error("Backend returned empty Excel file");
//         }

//         // =====================================
//         // DOWNLOAD
//         // =====================================
//         const downloadUrl = window.URL.createObjectURL(blob);
//         const link = document.createElement("a");
//         link.href = downloadUrl;
//         link.download = `${source.charAt(0).toUpperCase() + source.slice(1)}_Invoice_Output.xlsx`;
//         link.style.display = "none";

//         document.body.appendChild(link);
//         link.click();

//         setTimeout(() => {
//             document.body.removeChild(link);
//             window.URL.revokeObjectURL(downloadUrl);
//         }, 1000);

//         status.innerText = "✅ Excel downloaded successfully";
//         status.style.color = "green";

//     } catch (error) {
//         console.error("Download Error:", error);
//         status.innerText = "❌ " + error.message;
//         status.style.color = "red";
//     } finally {
//         runBtn.disabled = false;
//     }
// }

// window.uploadFolder = uploadFolder;



// ==========================================
// INTERACTIVE DROPZONE VALIDATOR
// ==========================================
function updateFolderStatus() {
    const input = document.getElementById("folderInput");
    const display = document.getElementById("fileCountDisplay");
    const status = document.getElementById("status");
    
    if (input && input.files && input.files.length > 0) {
        let count = 0;
        for (const file of input.files) {
            if (file.name.toLowerCase().endsWith(".pdf")) {
                count++;
            }
        }
        
        if (display) {
            display.innerText = `Selected: ${count} documents queued`;
            display.style.color = '#16a34a';
        }
        
        if (status) {
            status.innerText = `📁 ${count} PDF files detected. Ready to extract!`;
            status.style.color = "#4b5563";
        }
    }
}

window.updateFolderStatus = updateFolderStatus;

// ==========================================
// API BULK UPLOAD EXCEL STREAMER
// ==========================================
async function uploadFolder() {
    const input = document.getElementById("folderInput");
    const sourceSelect = document.getElementById("sourceSelect");
    const status = document.getElementById("status");
    const runBtn = document.getElementById("runParserBtn");

    if (!input || !sourceSelect || !status || !runBtn) {
        alert("Layout elements missing.");
        return;
    }

    const files = input.files;
    if (!files || !files.length) {
        status.innerText = "⚠️ Please select a folder first";
        status.style.color = "red";
        return;
    }

    const formData = new FormData();
    let pdfCount = 0;

    for (const file of files) {
        if (file.name.toLowerCase().endsWith(".pdf")) {
            formData.append("files", file);
            pdfCount++;
        }
    }

    if (pdfCount === 0) {
        status.innerText = "⚠️ No PDF files found in this directory.";
        status.style.color = "red";
        return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
        alert("Session expired. Please login again.");
        window.location.href = "/pages/login.html";
        return;
    }

    const source = sourceSelect.value;
    const endpoint = `${API_BASE_URL}/${source}`;

    runBtn.disabled = true;
    status.innerText = `⏳ Uploading and processing ${pdfCount} documents...`;
    status.style.color = "#2563eb";

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });

        if (!response.ok) {
            let message = "Parsing failed.";
            try {
                const errData = await response.json();
                message = errData.detail || message;
            } catch(e) {}
            throw new Error(message);
        }

        const blob = await response.blob();
        if (blob.size <= 0) {
            throw new Error("Empty worksheet response from engine.");
        }

        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = downloadUrl;
        link.download = `${source.toUpperCase()}_Report_${Date.now()}.xlsx`;
        document.body.appendChild(link);
        link.click();

        setTimeout(() => {
            document.body.removeChild(link);
            window.URL.revokeObjectURL(downloadUrl);
        }, 1000);

        status.innerText = "✅ Excel sheet generated and downloaded successfully!";
        status.style.color = "green";

    } catch (error) {
        console.error("Processing pipeline error:", error);
        status.innerText = `❌ ${error.message}`;
        status.style.color = "red";
    } finally {
        runBtn.disabled = false;
    }
}

window.uploadFolder = uploadFolder;