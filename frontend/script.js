// async function uploadFolder() {

//     const input =
//         document.getElementById("folderInput");

//     const status =
//         document.getElementById("status");

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

//     try {

//         const response = await fetch(
//             "https://reconova-983m.onrender.com/upload",
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

//         a.download =
//             "Amazon_Invoice_Output.xlsx";

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



async function uploadFolder() {

    const input =
        document.getElementById("folderInput");

    const status =
        document.getElementById("status");

    const sourceSelect =
        document.getElementById("sourceSelect");

    const files = input.files;

    if (files.length === 0) {

        alert("Please select folder");
        return;
    }

    const formData = new FormData();

    let pdfCount = 0;

    for (let file of files) {

        if (
            file.name
            .toLowerCase()
            .endsWith(".pdf")
        ) {

            formData.append(
                "files",
                file
            );

            pdfCount++;
        }
    }

    if (pdfCount === 0) {

        alert("No PDF files found");
        return;
    }

    status.innerText =
        `Uploading ${pdfCount} PDF files...`;

    const sourceValue = sourceSelect.value;

    try {

        const response = await fetch(
            `https://reconova-983m.onrender.com/upload?source=${sourceValue}`,
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {

            throw new Error(
                "Excel generation failed"
            );
        }

        status.innerText =
            "Generating Excel...";

        const blob =
            await response.blob();

        const url =
            window.URL.createObjectURL(blob);

        const a =
            document.createElement("a");

        a.href = url;

        const formattedSource = 
            sourceValue.charAt(0).toUpperCase() + sourceValue.slice(1);

        a.download =
            `${formattedSource}_Invoice_Output.xlsx`;

        document.body.appendChild(a);

        a.click();

        a.remove();

        status.innerText =
            "Excel downloaded successfully";
    }

    catch (error) {

        console.error(error);

        status.innerText =
            "Error occurred";
    }
}