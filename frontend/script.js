async function uploadFolder() {

    const input =
        document.getElementById("folderInput");

    const status =
        document.getElementById("status");

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

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/upload",
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

        a.download =
            "Amazon_Invoice_Output.xlsx";

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