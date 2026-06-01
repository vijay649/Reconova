
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from typing import List

import os
import shutil
import fitz
import pandas as pd
import re

from openpyxl import load_workbook

# app = FastAPI()

# =====================================================
# CORS
# =====================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# =====================================================
# FOLDERS
# =====================================================

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if text is None:
        return ""

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# =====================================================
# CLEAN NUMBER
# =====================================================

def clean_number(value):

    if not value:
        return 0.0

    value = str(value)

    value = value.replace("INR", "")
    value = value.replace("-INR", "-")
    value = value.replace(",", "")
    value = value.strip()

    try:
        return float(value)

    except:
        return 0.0

# =====================================================
# EXTRACT REGEX
# =====================================================

def extract(pattern, text):

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return clean_text(match.group(1))

    return ""

# =====================================================
# HOME
# =====================================================

# @app.get("/")
# def home():

#     return {
#         "message": "Amazon Invoice OCR API Running"
#     }

# =====================================================
# UPLOAD API
# =====================================================

async def upload_amazon(
    files: List[UploadFile] = File(...)
):

    results = []

    # =================================================
    # LOOP FILES
    # =================================================

    for file in files:

        try:

            print(f"Processing: {file.filename}")

            # =============================================
            # SAFE FILE NAME
            # =============================================

            safe_filename = os.path.basename(file.filename)

            safe_filename = safe_filename.replace("/", "_")
            safe_filename = safe_filename.replace("\\", "_")

            # =============================================
            # SAVE PATH
            # =============================================

            save_path = os.path.join(
                UPLOAD_FOLDER,
                safe_filename
            )

            # =============================================
            # SAVE FILE
            # =============================================

            with open(save_path, "wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer
                )

            print(f"Saved Successfully: {save_path}")

            # =============================================
            # OPEN PDF
            # =============================================

            doc = fitz.open(save_path)

            full_text = ""

            for page in doc:

                full_text += page.get_text()

            doc.close()

            # =============================================
            # CLEAN TEXT
            # =============================================

            normalized_text = clean_text(full_text)

            normalized_text = normalized_text.split(
                "Details of Fees to the above"
            )[0]

            # =============================================
            # DOCUMENT TYPE
            # =============================================

            document_type = "Invoice"

            if "Credit Note" in normalized_text:
                document_type = "Credit Note"

            # =============================================
            # COMPANY
            # =============================================

            company_name = extract(
                r'(Amazon Seller Services Private Limited|Amazon Retail India Private Limited)',
                normalized_text
            )

            company_gstin = extract(
                r'GST Tax Registration No:\s*([A-Z0-9]+)',
                normalized_text
            )

            # =============================================
            # INVOICE DETAILS
            # =============================================

            invoice_no = extract(
                r'(?:Invoice Number|Credit Note Number)\s*:\s*([A-Z0-9\-]+)',
                normalized_text
            )

            invoice_date = extract(
                r'(?:Invoice Date|Credit Note Date)\s*:\s*([0-9\/\-]+)',
                normalized_text
            )

            invoice_total = extract(
                r'Total(?: Invoice amount)?\s*:?\s*INR\s*([0-9,]+\.\d+)',
                normalized_text
            )

            invoice_total = clean_number(
                invoice_total
            )

            # =============================================
            # CUSTOMER
            # =============================================

            customer_name = extract(
                r'Bill to\s*Name:\s*(.*?)Address:',
                normalized_text
            )

            customer_gstin = extract(
                r'GSTIN:\s*([A-Z0-9]+)',
                normalized_text
            )

            # =============================================
            # ITEM ROWS
            # =============================================

            row_pattern = re.compile(

                r'(\d+)\.\s+'
                r'(\d{6})\s+'
                r'(.*?)\s+'
                r'INR\s*([0-9,]+\.\d+)'
                r'(.*?)'
                r'(?=\d+\.\s+\d{6}|\Z)',

                re.IGNORECASE | re.DOTALL
            )

            matches = row_pattern.findall(
                normalized_text
            )

            print(f"Rows Found: {len(matches)}")

            # =============================================
            # LOOP ROWS
            # =============================================

            for row in matches:

                (
                    serial_no,
                    sac_code,
                    description,
                    fee_amount,
                    tax_text
                ) = row

                description = clean_text(
                    description
                )

                fee_amount = clean_number(
                    fee_amount
                )

                sgst_rate = 0.0
                sgst_amount = 0.0

                cgst_rate = 0.0
                cgst_amount = 0.0

                igst_rate = 0.0
                igst_amount = 0.0

                # =========================================
                # SGST
                # =========================================

                sgst_match = re.search(
                    r'SGST\s*([0-9\.]+)%\s*INR\s*([0-9,]+\.\d+)',
                    tax_text
                )

                if sgst_match:

                    sgst_rate = clean_number(
                        sgst_match.group(1)
                    )

                    sgst_amount = clean_number(
                        sgst_match.group(2)
                    )

                # =========================================
                # CGST
                # =========================================

                cgst_match = re.search(
                    r'CGST\s*([0-9\.]+)%\s*INR\s*([0-9,]+\.\d+)',
                    tax_text
                )

                if cgst_match:

                    cgst_rate = clean_number(
                        cgst_match.group(1)
                    )

                    cgst_amount = clean_number(
                        cgst_match.group(2)
                    )

                # =========================================
                # IGST
                # =========================================

                igst_match = re.search(
                    r'IGST\s*([0-9\.]+)%\s*INR\s*([0-9,]+\.\d+)',
                    tax_text
                )

                if igst_match:

                    igst_rate = clean_number(
                        igst_match.group(1)
                    )

                    igst_amount = clean_number(
                        igst_match.group(2)
                    )

                # =========================================
                # LINE TOTAL
                # =========================================

                line_total = round(

                    fee_amount +
                    sgst_amount +
                    cgst_amount +
                    igst_amount,

                    2
                )

                # =========================================
                # APPEND RESULT
                # =========================================

                results.append({

                    "File Name": safe_filename,

                    "Document Type": document_type,

                    "Invoice No": invoice_no,
                    "Invoice Date": invoice_date,

                    "Company Name": company_name,
                    "Company GSTIN": company_gstin,

                    "Customer Name": customer_name,
                    "Customer GSTIN": customer_gstin,

                    "SAC Code": sac_code,

                    "Description": description,

                    "Fee Amount": fee_amount,

                    "SGST Rate": sgst_rate,
                    "SGST Amount": sgst_amount,

                    "CGST Rate": cgst_rate,
                    "CGST Amount": cgst_amount,

                    "IGST Rate": igst_rate,
                    "IGST Amount": igst_amount,

                    "Line Total": line_total,

                    "Invoice Total": invoice_total
                })

        except Exception as e:

            print("=" * 50)
            print(f"ERROR FILE: {file.filename}")
            print(str(e))
            print("=" * 50)

    # =================================================
    # CREATE DATAFRAME
    # =================================================

    df = pd.DataFrame(results)

    # =================================================
    # EMPTY CHECK
    # =================================================

    if df.empty:

        df = pd.DataFrame([
            {
                "Message": "No Data Found"
            }
        ])

    # =================================================
    # OUTPUT EXCEL FILE
    # =================================================

    output_file = os.path.join(
        OUTPUT_FOLDER,
        "Amazon_Invoice_Output.xlsx"
    )

    # DELETE OLD FILE
    if os.path.exists(output_file):
        os.remove(output_file)

    # =================================================
    # SAVE EXCEL
    # =================================================

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Invoices"
        )

    # =================================================
    # VALIDATE EXCEL
    # =================================================

    wb = load_workbook(output_file)

    ws = wb.active

    # AUTO WIDTH
    for column_cells in ws.columns:

        length = max(

            len(str(cell.value))
            if cell.value else 0

            for cell in column_cells
        )

        ws.column_dimensions[
            column_cells[0].column_letter
        ].width = length + 5

    wb.save(output_file)
    wb.close()

    print(f"Excel Created: {output_file}")

    # =================================================
    # RETURN FILE
    # =================================================

    return FileResponse(
        path=output_file,
        filename="Amazon_Invoice_Output.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    