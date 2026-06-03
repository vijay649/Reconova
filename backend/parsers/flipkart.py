
# import fitz
# import pandas as pd
# import re
# import os

# from tkinter import Tk
# from tkinter.filedialog import askdirectory
# from tkinter import messagebox

# # =====================================
# # FOLDER PICKER
# # =====================================

# Tk().withdraw()

# folder_path = askdirectory(
#     title="Select Flipkart Invoice Folder"
# )

# if not folder_path:
#     print("No folder selected")
#     exit()

# results = []

# # =====================================
# # HELPERS
# # =====================================

# def clean_text(text):

#     if not text:
#         return ""

#     text = text.replace("\n", " ")
#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# def clean_number(value):

#     if not value:
#         return 0.0

#     value = str(value)

#     value = value.replace(",", "")
#     value = value.replace("Rs.", "")
#     value = value.strip()

#     try:
#         return float(value)

#     except:
#         return 0.0


# def extract(pattern, text):

#     match = re.search(
#         pattern,
#         text,
#         re.IGNORECASE | re.DOTALL
#     )

#     if match:
#         return clean_text(match.group(1))

#     return ""


# # =====================================
# # PROCESS FILES
# # =====================================

# for root, dirs, files in os.walk(folder_path):

#     for file in files:

#         if not file.lower().endswith(".pdf"):
#             continue

#         full_path = os.path.join(root, file)

#         print(f"Processing: {file}")

#         try:

#             doc = fitz.open(full_path)

#             full_text = ""

#             for page in doc:
#                 full_text += page.get_text()

#             text = clean_text(full_text)

#             # =================================
#             # DOCUMENT TYPE
#             # =================================

#             document_type = "Invoice"

#             if "Commercial Credit Note" in text:
#                 document_type = "Credit Note"

#             # =================================
#             # COMPANY DETAILS
#             # =================================

#             company_name = extract(
#                 r'BILLED FROM:\s*(.*?)\s*(?:Tel:|GSTIN:|CIN:)',
#                 text
#             )

#             company_gstin = extract(
#                 r'GSTIN:\s*([A-Z0-9]+)',
#                 text
#             )

#             # =================================
#             # CUSTOMER DETAILS
#             # =================================

#             customer_name = extract(
#                 r'Business Name:\s*(.*?)\s*Address:',
#                 text
#             )

#             customer_gstin = extract(
#                 r'BILLED TO:.*?GSTIN:\s*([A-Z0-9]+)',
#                 text
#             )

#             # =================================
#             # DOCUMENT DETAILS
#             # =================================

#             invoice_no = extract(
#                 r'Invoice #:\s*([A-Z0-9]+)',
#                 text
#             )

#             invoice_date = extract(
#                 r'Invoice Date:\s*([0-9\-\/]+)',
#                 text
#             )

#             credit_no = extract(
#                 r'Credit Note #:\s*([A-Z0-9]+)',
#                 text
#             )

#             credit_date = extract(
#                 r'Credit Note Date:\s*([0-9\-\/]+)',
#                 text
#             )

#             # =================================
#             # TOTAL VALUE
#             # =================================

#             invoice_total = extract(
#                 r'Total\s+([0-9,]+\.\d+)\s*$',
#                 text
#             )

#             invoice_total = clean_number(invoice_total)

#             # =================================
#             # INVOICE ROWS
#             # =================================

#             if document_type == "Invoice":

#                 row_pattern = re.compile(

#                     r'(\d{6})\s+'
#                     r'(.*?)\s+'
#                     r'([0-9,]+\.\d+)\s+'
#                     r'([0-9.]+)\s+'
#                     r'([0-9,]+\.\d+)\s+'
#                     r'([0-9,]+\.\d+)',

#                     re.IGNORECASE
#                 )

#                 matches = row_pattern.findall(text)

#                 for row in matches:

#                     (
#                         sac_code,
#                         description,
#                         taxable_value,
#                         igst_rate,
#                         igst_amount,
#                         total_amount
#                     ) = row

#                     results.append({

#                         "File Name": file,

#                         "Document Type": document_type,

#                         "Invoice No": invoice_no,
#                         "Invoice Date": invoice_date,

#                         "Company Name": company_name,
#                         "Company GSTIN": company_gstin,

#                         "Customer Name": customer_name,
#                         "Customer GSTIN": customer_gstin,

#                         "SAC Code": sac_code,
#                         "Description": clean_text(description),

#                         "Taxable Value":
#                             clean_number(taxable_value),

#                         "IGST Rate":
#                             clean_number(igst_rate),

#                         "IGST Amount":
#                             clean_number(igst_amount),

#                         "Line Total":
#                             clean_number(total_amount),

#                         "Invoice Total":
#                             invoice_total
#                     })

#             # =================================
#             # CREDIT NOTE
#             # =================================

#             else:

#                 credit_pattern = re.compile(

#                     r'(\d+)\s+'
#                     r'(.*?)\s+'
#                     r'([0-9,]+\.\d+)',

#                     re.IGNORECASE
#                 )

#                 matches = credit_pattern.findall(text)

#                 for row in matches:

#                     (
#                         sr_no,
#                         description,
#                         amount
#                     ) = row

#                     amount = -abs(
#                         clean_number(amount)
#                     )

#                     results.append({

#                         "File Name": file,

#                         "Document Type": document_type,

#                         "Credit Note No": credit_no,
#                         "Credit Note Date": credit_date,

#                         "Company Name": company_name,

#                         "Customer Name": customer_name,

#                         "Description":
#                             clean_text(description),

#                         "Amount": amount
#                     })

#         except Exception as e:

#             print(f"Error processing {file}")
#             print(str(e))

# # =====================================
# # DATAFRAME
# # =====================================

# df = pd.DataFrame(results)

# # =====================================
# # OUTPUT
# # =====================================

# output_file = os.path.join(
#     folder_path,
#     "Flipkart_Invoice_Output.xlsx"
# )

# with pd.ExcelWriter(
#     output_file,
#     engine="openpyxl"
# ) as writer:

#     df.to_excel(
#         writer,
#         index=False
#     )

#     ws = writer.sheets["Sheet1"]

#     for row in ws.iter_rows(min_row=2):

#         for cell in row:

#             if isinstance(
#                 cell.value,
#                 (int, float)
#             ):
#                 cell.number_format = "0.00"

# root = Tk()
# root.withdraw()

# messagebox.showinfo(
#     "Completed",
#     f"Flipkart Extraction Completed\n\n{output_file}"
# )

# print("=================================")
# print("Flipkart Extraction Completed")
# print("=================================")
# print(output_file)


from fastapi import UploadFile, File
from fastapi.responses import FileResponse
 
import fitz
import pandas as pd
import re
import os
import uuid
 
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
# -------------------------------
# HELPERS
# -------------------------------
def clean_text(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
 
 
def clean_number(value):
    if not value:
        return 0.0
    value = str(value).replace(",", "").replace("₹", "").replace("Rs.", "")
    try:
        return float(value.strip())
    except:
        return 0.0
 
 
def extract(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""
 
 
# -------------------------------
# MAIN API
# -------------------------------
async def upload_flipkart(files: list[UploadFile] = File(...)):
    results = []
 
    for file in files:
 
        if not file.filename.lower().endswith(".pdf"):
            continue
 
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
 
        full_text = ""
        for page in doc:
            full_text += page.get_text()
 
        doc.close()
        text = clean_text(full_text)
 
        # -------------------------------
        # COMMON DATA
        # -------------------------------
        company_name = extract(
            r'BILLED FROM:\s*(.*?)\s*(?:Tel:|GSTIN:|CIN:)', text
        )
 
        company_gstin = extract(
            r'BILLED FROM:.*?GSTIN:\s*([A-Z0-9]{15})', text
        )
 
        customer_name = extract(
            r'Business Name:\s*(.*?)\s*Address:', text
        )
 
        customer_gstin = extract(
            r'BILLED TO:.*?GSTIN:\s*([A-Z0-9]{15})', text
        )
 
        invoice_no = extract(
            r'Invoice\s*#:\s*([A-Z0-9\-\/]+)', text
        )
 
        invoice_date = extract(
            r'Invoice Date:\s*([0-9\-\/]+)', text
        )
 
        # -------------------------------
        # CREDIT NOTE CHECK
        # -------------------------------
        is_credit_note = "Credit Note" in text
 
        # ==================================
        # ✅ CREDIT NOTE BLOCK
        # ==================================
        if is_credit_note:
 
            credit_no = extract(
                r'Credit Note\s*#:\s*([A-Z0-9\-\/]+)', text
            )
 
            credit_date = extract(
                r'Credit Note Date:\s*([0-9\-\/]+)', text
            )
 
            description = extract(
                r'Particulars:\s*(.*?)\s*BILLED TO:', text
            )
 
            # Total from credit note
            amount = extract(r'Total\s+([0-9,]+\.\d+)', text)
            amount = -abs(clean_number(amount))
 
            results.append({
                "File Name": file.filename,
                "Document Type": "Credit Note",
 
                "Invoice No": "",
                "Invoice Date": "",
 
                "Company Name": company_name,
                "Company GSTIN": company_gstin,
 
                "Customer Name": customer_name,
                "Customer GSTIN": customer_gstin,
 
                "SAC Code": "",
                "Description": description,
 
                "Taxable Value": "",
                "IGST Rate": "",
                "IGST Amount": "",
                "Line Total": "",
 
                "Invoice Total": "",
 
                "Credit Note No": credit_no,
                "Credit Note Date": credit_date,
 
                "Amount": amount
            })
 
        # ==================================
        # ✅ INVOICE BLOCK
        # ==================================
        else:
 
            # Invoice total (last total line)
            invoice_total = extract(
                r'Total\s+[0-9,]+\.\d+\s+[0-9,]+\.\d+\s+([0-9,]+\.\d+)',
                text
            )
 
            # -------------------------
            # IGST FORMAT
            # -------------------------
            igst_pattern = re.compile(
                r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
                re.IGNORECASE
            )
 
            # -------------------------
            # CGST + SGST FORMAT
            # -------------------------
            cgst_pattern = re.compile(
                r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
                re.IGNORECASE
            )
 
            igst_rows = igst_pattern.findall(text)
            cgst_rows = cgst_pattern.findall(text)
 
            # -------------------------
            # ✅ IGST ROWS
            # -------------------------
            for row in igst_rows:
                sac, desc, taxable, rate, tax_amt, total = row
 
                results.append({
                    "File Name": file.filename,
                    "Document Type": "Invoice",
 
                    "Invoice No": invoice_no,
                    "Invoice Date": invoice_date,
 
                    "Company Name": company_name,
                    "Company GSTIN": company_gstin,
 
                    "Customer Name": customer_name,
                    "Customer GSTIN": customer_gstin,
 
                    "SAC Code": sac,
                    "Description": clean_text(desc),
 
                    "Taxable Value": clean_number(taxable),
                    "IGST Rate": clean_number(rate),
                    "IGST Amount": clean_number(tax_amt),
 
                    "Line Total": clean_number(total),
                    "Invoice Total": clean_number(invoice_total),
 
                    "Credit Note No": "",
                    "Credit Note Date": "",
                    "Amount": ""
                })
 
            # -------------------------
            # ✅ CGST + SGST ROWS
            # (convert to IGST)
            # -------------------------
            for row in cgst_rows:
                sac, desc, taxable, cgst_rate, sgst_rate, cgst_amt, sgst_amt = row
 
                igst_rate = clean_number(cgst_rate) + clean_number(sgst_rate)
                igst_amt = clean_number(cgst_amt) + clean_number(sgst_amt)
 
                total = clean_number(taxable) + igst_amt
 
                results.append({
                    "File Name": file.filename,
                    "Document Type": "Invoice",
 
                    "Invoice No": invoice_no,
                    "Invoice Date": invoice_date,
 
                    "Company Name": company_name,
                    "Company GSTIN": company_gstin,
 
                    "Customer Name": customer_name,
                    "Customer GSTIN": customer_gstin,
 
                    "SAC Code": sac,
                    "Description": clean_text(desc),
 
                    "Taxable Value": clean_number(taxable),
 
                    "IGST Rate": igst_rate,
                    "IGST Amount": igst_amt,
 
                    "Line Total": total,
                    "Invoice Total": clean_number(invoice_total),
 
                    "Credit Note No": "",
                    "Credit Note Date": "",
                    "Amount": ""
                })
 
    # -------------------------------
    # FINAL DATAFRAME (ORDER FIXED)
    # -------------------------------
    df = pd.DataFrame(results)
 
    df = df[[
        "File Name",
        "Document Type",
        "Invoice No",
        "Invoice Date",
        "Company Name",
        "Company GSTIN",
        "Customer Name",
        "Customer GSTIN",
        "SAC Code",
        "Description",
        "Taxable Value",
        "IGST Rate",
        "IGST Amount",
        "Line Total",
        "Invoice Total",
        "Credit Note No",
        "Credit Note Date",
        "Amount"
    ]]
 
    output_file = os.path.join(
        OUTPUT_DIR,
        f"flipkart_{uuid.uuid4()}.xlsx"
    )
 
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
 
    return FileResponse(
        output_file,
        filename="Flipkart_Invoice_Output.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )