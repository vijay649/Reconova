// async function uploadFolder() {

//     const input =
//         document.getElementById("folderInput");

//     const status =
//         document.getElementById("status");

//     const sourceSelect =
//         document.getElementById("sourceSelect");

//     const files = input.files;

//     if (files.length === 0) {

//         alert("Please select folder");
//         return;
//     }

//     const formData = new FormData();

//     let pdfCount = 0;

//     for (let file of files) {

//         if (
//             file.name
//             .toLowerCase()
//             .endsWith(".pdf")
//         ) {

//             formData.append(
//                 "files",
//                 file
//             );

//             pdfCount++;
//         }
//     }

//     if (pdfCount === 0) {

//         alert("No PDF files found");
//         return;
//     }

//     status.innerText =
//         `Uploading ${pdfCount} PDF files...`;

//     const sourceValue = sourceSelect.value;

//     try {

//         const response = await fetch(
//             `https://reconova-983m.onrender.com/upload?source=${sourceValue}`,
//             {
//                 method: "POST",
//                 body: formData
//             }
//         );

//         if (!response.ok) {

//             throw new Error(
//                 "Excel generation failed"
//             );
//         }

//         status.innerText =
//             "Generating Excel...";

//         const blob =
//             await response.blob();

//         const url =
//             window.URL.createObjectURL(blob);

//         const a =
//             document.createElement("a");

//         a.href = url;

//         const formattedSource = 
//             sourceValue.charAt(0).toUpperCase() + sourceValue.slice(1);

//         a.download =
//             `${formattedSource}_Invoice_Output.xlsx`;

//         document.body.appendChild(a);

//         a.click();

//         a.remove();

//         status.innerText =
//             "Excel downloaded successfully";
//     }

//     catch (error) {

//         console.error(error);

//         status.innerText =
//             "Error occurred";
//     }
// }

// async function uploadFolder() {
//     const input = document.getElementById("folderInput");
//     const status = document.getElementById("status");
//     const sourceSelect = document.getElementById("sourceSelect");
//     const files = input.files;

//     if (files.length === 0) {
//         alert("Please select folder");
//         return;
//     }

//     const formData = new FormData();
//     let pdfCount = 0;

//     for (let file of files) {
//         if (file.name.toLowerCase().endsWith(".pdf")) {
//             formData.append("files", file);
//             pdfCount++;
//         }
//     }

//     if (pdfCount === 0) {
//         alert("No PDF files found");
//         return;
//     }

//     status.innerText = `Uploading ${pdfCount} PDF files...`;
//     const sourceValue = sourceSelect.value;

//     try {
//         // Aapka dropdown ka select value Render ke URL me query parameter bankar jayega
//         const response = await fetch(
//             // `https://reconova-983m.onrender.com/upload?source=${sourceValue}`,
//             'http://localhost:8000/swiggy',
//             {
//                 method: "POST",
//                 body: formData
//             }
//         );

//         if (!response.ok) {
//             throw new Error("Excel generation failed");
//         }

//         status.innerText = "Generating Excel...";
//         const blob = await response.blob();
//         const url = window.URL.createObjectURL(blob);
//         const a = document.createElement("a");
//         a.href = url;

//         const formattedSource = sourceValue.charAt(0).toUpperCase() + sourceValue.slice(1);
//         a.download = `${formattedSource}_Invoice_Output.xlsx`;
//         document.body.appendChild(a);
//         a.click();
//         a.remove();

//         status.innerText = "Excel downloaded successfully";
//     } catch (error) {
//         console.error(error);
//         status.innerText = "Error occurred";
//     }
// }

// async function uploadFolder() {

//     const input = document.getElementById("folderInput");
//     const status = document.getElementById("status");
//     const sourceSelect = document.getElementById("sourceSelect");

//     const files = input.files;

//     if (files.length === 0) {
//         alert("Please select folder");
//         return;
//     }

//     const formData = new FormData();

//     let pdfCount = 0;

//     for (let file of files) {

//         if (file.name.toLowerCase().endsWith(".pdf")) {

//             formData.append("files", file);
//             pdfCount++;
//         }
//     }

//     if (pdfCount === 0) {
//         alert("No PDF files found");
//         return;
//     }

//     const sourceValue = sourceSelect.value;

//     status.innerText = `Uploading ${pdfCount} PDF files...`;

//     try {

//         const apiUrl = `http://localhost:8000/${sourceValue}`;

//         console.log("Calling API:", apiUrl);

//         const response = await fetch(
//             apiUrl,
//             {
//                 method: "POST",
//                 body: formData
//             }
//         );

//         if (!response.ok) {

//             const errorText = await response.text();

//             console.error(errorText);

//             throw new Error("Excel generation failed");
//         }

//         status.innerText = "Generating Excel...";

//         const blob = await response.blob();

//         const url = window.URL.createObjectURL(blob);

//         const a = document.createElement("a");

//         a.href = url;

//         a.download = `${sourceValue}_Invoice_Output.xlsx`;

//         document.body.appendChild(a);

//         a.click();

//         a.remove();

//         window.URL.revokeObjectURL(url);

//         status.innerText = "Excel downloaded successfully";

//     }
//     catch (error) {

//         console.error(error);

//         status.innerText = error.message;
//     }
// }

async function uploadFolder() {

    const input = document.getElementById("folderInput");
    const sourceSelect = document.getElementById("sourceSelect");
    const status = document.getElementById("status");

    const files = input.files;

    if (files.length === 0) {
        alert("Please select folder");
        return;
    }

    const formData = new FormData();

    let pdfCount = 0;

    for (let file of files) {

        if (file.name.toLowerCase().endsWith(".pdf")) {

            formData.append("files", file);

            pdfCount++;
        }
    }

    if (pdfCount === 0) {

        alert("No PDF files found");
        return;
    }

    const source = sourceSelect.value;

    const apiMap = {
        amazon: "https://reconova-983m.onrender.com/amazon",
        swiggy: "https://reconova-983m.onrender.com/swiggy",
        zomato: "https://reconova-983m.onrender.com/zomato",
        blinkit: "http://localhost:8000/blinkit",
        flipkart: "http://localhost:8000/flipkart"
    };

    const endpoint = apiMap[source];

    try {

        status.innerText = `Uploading ${pdfCount} PDFs...`;

        const response = await fetch(endpoint, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Excel generation failed");
        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;

        a.download =
            source.charAt(0).toUpperCase() +
            source.slice(1) +
            "_Invoice_Output.xlsx";

        document.body.appendChild(a);

        a.click();

        a.remove();

        status.innerText = "Excel downloaded successfully";

    } catch (error) {

        console.error(error);

        status.innerText = "Error occurred";
    }
}