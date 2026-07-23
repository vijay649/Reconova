# from fastapi import Depends

# from sqlalchemy.orm import Session

# from auth.dependencies import get_current_user

# from database.database import get_db

# from database.models import UploadAnalytics, User


# from fastapi import UploadFile, File
# from fastapi.responses import FileResponse
 
# import fitz
# import pandas as pd
# import re
# import os
# import uuid
 
# OUTPUT_DIR = "output"
# os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
# # ---------------------------
# # HELPERS
# # ---------------------------
# def clean_text(text):
#     if not text:
#         return ""
#     return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
 
 
# def clean_number(value):
#     if not value:
#         return 0.0
#     value = str(value).replace(",", "").replace("₹", "").replace("Rs.", "")
#     try:
#         return float(value.strip())
#     except:
#         return 0.0
 
 
# def extract(pattern, text):
#     match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
#     return clean_text(match.group(1)) if match else ""
 
 
# # ---------------------------
# # MAIN API
# # ---------------------------
# async def upload_flipkart(files: list[UploadFile] = File(...),
#         db: Session = Depends(get_db),

#         current_user: User = Depends(
#             get_current_user
#         )
#     ):
    
#     files_count = len(files)
 
#     results = []
 
#     for file in files:
 
#         if not file.filename.lower().endswith(".pdf"):
#             continue
 
#         pdf_bytes = await file.read()
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")
 
#         full_text = ""
#         for page in doc:
#             full_text += page.get_text()
 
#         doc.close()
 
#         text = clean_text(full_text)
 
#         # ---------------------------
#         # COMMON FIELDS
#         # ---------------------------
#         company_name = extract(r'BILLED FROM:\s*(.*?)\s*(?:Tel:|GSTIN:|CIN:)', text)
#         company_gstin = extract(r'BILLED FROM:.*?GSTIN:\s*([A-Z0-9]{15})', text)
#         customer_name = extract(r'Business Name:\s*(.*?)\s*Address:', text)
#         customer_gstin = extract(r'BILLED TO:.*?GSTIN:\s*([A-Z0-9]{15})', text)
 
#         invoice_no = extract(r'Invoice\s*#:\s*([A-Z0-9\-\/]+)', text)
#         invoice_date = extract(r'Invoice Date:\s*([0-9\-\/]+)', text)
 
#         is_credit_note = "Credit Note" in text
 
#         # ===================================================
#         # ✅ CREDIT NOTE
#         # ===================================================
#         if is_credit_note:
 
#             credit_no = extract(r'Credit Note\s*#:\s*([A-Z0-9\-\/]+)', text)
#             credit_date = extract(r'Credit Note Date:\s*([0-9\-\/]+)', text)
#             description = extract(r'Particulars:\s*(.*?)\s*BILLED TO:', text)
 
#             amount = extract(r'Total\s+([0-9,]+\.\d+)', text)
#             amount = -abs(clean_number(amount))
 
#             results.append({
#                 "File Name": file.filename,
#                 "Document Type": "Credit Note",
#                 "Invoice No": "",
#                 "Invoice Date": "",
#                 "Company Name": company_name,
#                 "Company GSTIN": company_gstin,
#                 "Customer Name": customer_name,
#                 "Customer GSTIN": customer_gstin,
#                 "SAC Code": "",
#                 "Description": description,
#                 "Taxable Value": "",
#                 "IGST Rate": "",
#                 "IGST Amount": "",
#                 "CGST Rate": "",
#                 "CGST Amount": "",
#                 "SGST Rate": "",
#                 "SGST Amount": "",
#                 "Line Total": "",
#                 "Invoice Total": "",
#                 "Credit Note No": credit_no,
#                 "Credit Note Date": credit_date,
#                 "Amount": amount
#             })
 
#         # ===================================================
#         # ✅ INVOICE
#         # ===================================================
#         else:
 
#             # Detect tax type correctly
#             has_cgst = "CGST Rate" in text and "SGST Rate" in text
#             has_igst = "IGST Rate" in text
 
#             # ✅ FIXED invoice total extraction
#             invoice_total_match = re.search(
#                 r'Total\s+[0-9,]+\.\d+\s+[0-9,]+\.\d+\s+[0-9,]+\.\d+\s+([0-9,]+\.\d+)',
#                 text
#             )
#             invoice_total = clean_number(invoice_total_match.group(1)) if invoice_total_match else 0.0
 
#             # ---------------------------------
#             # ✅ CGST + SGST (ONLY)
#             # ---------------------------------
#             if has_cgst:
 
#                 cgst_pattern = re.compile(
#                     r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
#                     re.IGNORECASE
#                 )
 
#                 rows = cgst_pattern.findall(text)
 
#                 for row in rows:
#                     sac, desc, taxable, cgst_rate, sgst_rate, cgst_amt, sgst_amt = row
 
#                     results.append({
#                         "File Name": file.filename,
#                         "Document Type": "Invoice",
#                         "Invoice No": invoice_no,
#                         "Invoice Date": invoice_date,
#                         "Company Name": company_name,
#                         "Company GSTIN": company_gstin,
#                         "Customer Name": customer_name,
#                         "Customer GSTIN": customer_gstin,
#                         "SAC Code": sac,
#                         "Description": clean_text(desc),
#                         "Taxable Value": clean_number(taxable),
 
#                         "IGST Rate": 0,
#                         "IGST Amount": 0,
 
#                         "CGST Rate": clean_number(cgst_rate),
#                         "CGST Amount": clean_number(cgst_amt),
#                         "SGST Rate": clean_number(sgst_rate),
#                         "SGST Amount": clean_number(sgst_amt),
 
#                         "Line Total": (
#                             clean_number(taxable)
#                             + clean_number(cgst_amt)
#                             + clean_number(sgst_amt)
#                         ),
 
#                         "Invoice Total": invoice_total,
 
#                         "Credit Note No": "",
#                         "Credit Note Date": "",
#                         "Amount": ""
#                     })
 
#             # ---------------------------------
#             # ✅ IGST ONLY
#             # ---------------------------------
#             elif has_igst:
 
#                 igst_pattern = re.compile(
#                     r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
#                     re.IGNORECASE
#                 )
 
#                 rows = igst_pattern.findall(text)
 
#                 for row in rows:
#                     sac, desc, taxable, rate, tax_amt, total = row
 
#                     results.append({
#                         "File Name": file.filename,
#                         "Document Type": "Invoice",
#                         "Invoice No": invoice_no,
#                         "Invoice Date": invoice_date,
#                         "Company Name": company_name,
#                         "Company GSTIN": company_gstin,
#                         "Customer Name": customer_name,
#                         "Customer GSTIN": customer_gstin,
#                         "SAC Code": sac,
#                         "Description": clean_text(desc),
#                         "Taxable Value": clean_number(taxable),
 
#                         "IGST Rate": clean_number(rate),
#                         "IGST Amount": clean_number(tax_amt),
 
#                         "CGST Rate": 0,
#                         "CGST Amount": 0,
#                         "SGST Rate": 0,
#                         "SGST Amount": 0,
 
#                         "Line Total": clean_number(total),
#                         "Invoice Total": invoice_total,
 
#                         "Credit Note No": "",
#                         "Credit Note Date": "",
#                         "Amount": ""
#                     })
 
#     # ---------------------------
#     # FINAL DATAFRAME
#     # ---------------------------
#     df = pd.DataFrame(results)
 
#     df = df[[
#         "File Name",
#         "Document Type",
#         "Invoice No",
#         "Invoice Date",
#         "Company Name",
#         "Company GSTIN",
#         "Customer Name",
#         "Customer GSTIN",
#         "SAC Code",
#         "Description",
#         "Taxable Value",
#         "IGST Rate",
#         "IGST Amount",
#         "CGST Rate",
#         "CGST Amount",
#         "SGST Rate",
#         "SGST Amount",
#         "Line Total",
#         "Invoice Total",
#         "Credit Note No",
#         "Credit Note Date",
#         "Amount"
#     ]]
 
#     output_file = os.path.join(
#         OUTPUT_DIR,
#         f"flipkart_{uuid.uuid4()}.xlsx"
#     )
 
#     with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
#         df.to_excel(writer, index=False)
        
#     if files_count > 0:

#         analytics = UploadAnalytics(

#             user_id=current_user.id,

#             source="flipkart",

#             pdf_count=files_count
#         )

#         db.add(analytics)

#         db.commit()
 
#     return FileResponse(
#         output_file,
#         filename="Flipkart_Invoice_Output.xlsx",
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     )





# import os
# import re
# import uuid
# import fitz
# import pandas as pd
# from typing import List

# from fastapi import Depends, UploadFile, File
# from fastapi.responses import FileResponse
# from sqlalchemy.orm import Session

# from database.database import get_db
# from database.models import UploadAnalytics

# OUTPUT_DIR = "output"
# os.makedirs(OUTPUT_DIR, exist_ok=True)


# # ---------------------------
# # HELPERS
# # ---------------------------
# def clean_text(text):
#     if not text:
#         return ""
#     return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()


# def clean_number(value):
#     if not value:
#         return 0.0
#     value = str(value).replace(",", "").replace("₹", "").replace("Rs.", "")
#     try:
#         return float(value.strip())
#     except:
#         return 0.0


# def extract(pattern, text):
#     match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
#     return clean_text(match.group(1)) if match else ""


# # ---------------------------
# # MAIN API
# # ---------------------------
# async def upload_flipkart(
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db),
#     current_user = None  # Removed model annotation & Depends() to prevent 401 and startup crashes
# ):
#     files_count = len(files)
#     results = []

#     for file in files:

#         if not file.filename.lower().endswith(".pdf"):
#             continue

#         pdf_bytes = await file.read()
#         doc = fitz.open(stream=pdf_bytes, filetype="pdf")

#         full_text = ""
#         for page in doc:
#             full_text += page.get_text()

#         doc.close()

#         text = clean_text(full_text)

#         # ---------------------------
#         # COMMON FIELDS
#         # ---------------------------
#         company_name = extract(r'BILLED FROM:\s*(.*?)\s*(?:Tel:|GSTIN:|CIN:)', text)
#         company_gstin = extract(r'BILLED FROM:.*?GSTIN:\s*([A-Z0-9]{15})', text)
#         customer_name = extract(r'Business Name:\s*(.*?)\s*Address:', text)
#         customer_gstin = extract(r'BILLED TO:.*?GSTIN:\s*([A-Z0-9]{15})', text)

#         invoice_no = extract(r'Invoice\s*#:\s*([A-Z0-9\-\/]+)', text)
#         invoice_date = extract(r'Invoice Date:\s*([0-9\-\/]+)', text)

#         is_credit_note = "Credit Note" in text

#         # ===================================================
#         # CREDIT NOTE
#         # ===================================================
#         if is_credit_note:

#             credit_no = extract(r'Credit Note\s*#:\s*([A-Z0-9\-\/]+)', text)
#             credit_date = extract(r'Credit Note Date:\s*([0-9\-\/]+)', text)
#             description = extract(r'Particulars:\s*(.*?)\s*BILLED TO:', text)

#             amount = extract(r'Total\s+([0-9,]+\.\d+)', text)
#             amount = -abs(clean_number(amount))

#             results.append({
#                 "File Name": file.filename,
#                 "Document Type": "Credit Note",
#                 "Invoice No": "",
#                 "Invoice Date": "",
#                 "Company Name": company_name,
#                 "Company GSTIN": company_gstin,
#                 "Customer Name": customer_name,
#                 "Customer GSTIN": customer_gstin,
#                 "SAC Code": "",
#                 "Description": description,
#                 "Taxable Value": "",
#                 "IGST Rate": "",
#                 "IGST Amount": "",
#                 "CGST Rate": "",
#                 "CGST Amount": "",
#                 "SGST Rate": "",
#                 "SGST Amount": "",
#                 "Line Total": "",
#                 "Invoice Total": "",
#                 "Credit Note No": credit_no,
#                 "Credit Note Date": credit_date,
#                 "Amount": amount
#             })

#         # ===================================================
#         # INVOICE
#         # ===================================================
#         else:

#             # Detect tax type correctly
#             has_cgst = "CGST Rate" in text and "SGST Rate" in text
#             has_igst = "IGST Rate" in text

#             # Invoice total extraction
#             invoice_total_match = re.search(
#                 r'Total\s+[0-9,]+\.\d+\s+[0-9,]+\.\d+\s+[0-9,]+\.\d+\s+([0-9,]+\.\d+)',
#                 text
#             )
#             invoice_total = clean_number(invoice_total_match.group(1)) if invoice_total_match else 0.0

#             # ---------------------------------
#             # CGST + SGST (ONLY)
#             # ---------------------------------
#             if has_cgst:

#                 cgst_pattern = re.compile(
#                     r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
#                     re.IGNORECASE
#                 )

#                 rows = cgst_pattern.findall(text)

#                 for row in rows:
#                     sac, desc, taxable, cgst_rate, sgst_rate, cgst_amt, sgst_amt = row

#                     results.append({
#                         "File Name": file.filename,
#                         "Document Type": "Invoice",
#                         "Invoice No": invoice_no,
#                         "Invoice Date": invoice_date,
#                         "Company Name": company_name,
#                         "Company GSTIN": company_gstin,
#                         "Customer Name": customer_name,
#                         "Customer GSTIN": customer_gstin,
#                         "SAC Code": sac,
#                         "Description": clean_text(desc),
#                         "Taxable Value": clean_number(taxable),

#                         "IGST Rate": 0,
#                         "IGST Amount": 0,

#                         "CGST Rate": clean_number(cgst_rate),
#                         "CGST Amount": clean_number(cgst_amt),
#                         "SGST Rate": clean_number(sgst_rate),
#                         "SGST Amount": clean_number(sgst_amt),

#                         "Line Total": (
#                             clean_number(taxable)
#                             + clean_number(cgst_amt)
#                             + clean_number(sgst_amt)
#                         ),

#                         "Invoice Total": invoice_total,

#                         "Credit Note No": "",
#                         "Credit Note Date": "",
#                         "Amount": ""
#                     })

#             # ---------------------------------
#             # IGST ONLY
#             # ---------------------------------
#             elif has_igst:

#                 igst_pattern = re.compile(
#                     r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
#                     re.IGNORECASE
#                 )

#                 rows = igst_pattern.findall(text)

#                 for row in rows:
#                     sac, desc, taxable, rate, tax_amt, total = row

#                     results.append({
#                         "File Name": file.filename,
#                         "Document Type": "Invoice",
#                         "Invoice No": invoice_no,
#                         "Invoice Date": invoice_date,
#                         "Company Name": company_name,
#                         "Company GSTIN": company_gstin,
#                         "Customer Name": customer_name,
#                         "Customer GSTIN": customer_gstin,
#                         "SAC Code": sac,
#                         "Description": clean_text(desc),
#                         "Taxable Value": clean_number(taxable),

#                         "IGST Rate": clean_number(rate),
#                         "IGST Amount": clean_number(tax_amt),

#                         "CGST Rate": 0,
#                         "CGST Amount": 0,
#                         "SGST Rate": 0,
#                         "SGST Amount": 0,

#                         "Line Total": clean_number(total),
#                         "Invoice Total": invoice_total,

#                         "Credit Note No": "",
#                         "Credit Note Date": "",
#                         "Amount": ""
#                     })

#     # ---------------------------
#     # FINAL DATAFRAME
#     # ---------------------------
#     df = pd.DataFrame(results)

#     if df.empty:
#         df = pd.DataFrame(columns=[
#             "File Name", "Document Type", "Invoice No", "Invoice Date",
#             "Company Name", "Company GSTIN", "Customer Name", "Customer GSTIN",
#             "SAC Code", "Description", "Taxable Value", "IGST Rate",
#             "IGST Amount", "CGST Rate", "CGST Amount", "SGST Rate",
#             "SGST Amount", "Line Total", "Invoice Total", "Credit Note No",
#             "Credit Note Date", "Amount"
#         ])
#     else:
#         df = df[[
#             "File Name",
#             "Document Type",
#             "Invoice No",
#             "Invoice Date",
#             "Company Name",
#             "Company GSTIN",
#             "Customer Name",
#             "Customer GSTIN",
#             "SAC Code",
#             "Description",
#             "Taxable Value",
#             "IGST Rate",
#             "IGST Amount",
#             "CGST Rate",
#             "CGST Amount",
#             "SGST Rate",
#             "SGST Amount",
#             "Line Total",
#             "Invoice Total",
#             "Credit Note No",
#             "Credit Note Date",
#             "Amount"
#         ]]

#     output_file = os.path.join(
#         OUTPUT_DIR,
#         f"flipkart_{uuid.uuid4()}.xlsx"
#     )

#     with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
#         df.to_excel(writer, index=False)
        
#     if files_count > 0 and current_user and hasattr(current_user, 'id'):
#         analytics = UploadAnalytics(
#             user_id=current_user.id,
#             source="flipkart",
#             pdf_count=files_count
#         )
#         db.add(analytics)
#         db.commit()

#     return FileResponse(
#         output_file,
#         filename="Flipkart_Invoice_Output.xlsx",
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     )








import os
import re
import gc
import tempfile
import shutil
from datetime import datetime
from typing import List

import pdfplumber
import pandas as pd
from fastapi import Depends, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UploadAnalytics


# ============================================
# HELPERS
# ============================================

def extract(pattern, text):
    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )
    return match.group(1).strip() if match else ""


def to_float(value):
    if not value:
        return 0.0
    try:
        return float(
            value.replace(",", "").strip()
        )
    except Exception:
        return 0.0


def remove_file(path: str):
    """Callback function to safely delete files after response delivery"""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


# ============================================
# PROCESS PDF
# ============================================

def process_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if not pdf.pages:
                pdf.close()
                return {"File Name": os.path.basename(pdf_path), "Error": "PDF is empty"}
            text = pdf.pages[0].extract_text() or ""
            pdf.close()  # Free memory resource immediately

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        invoice_no = extract(r"Invoice No[:\s]+([A-Z0-9\-]+)", text)
        invoice_date = extract(r"Invoice Date[:\s]+([0-9\-]+)", text)
        merchant_name = extract(r"Entity Name[:\s]+(.*?)\s+State", text)
        hsn_code = extract(r"HSN Code[:\s]+(\d+)", text)
        service_desc = extract(r"Service Description[:\s]+(.*?)\s+Work Description", text)

        period_start = ""
        period_end = ""

        period_match = re.search(
            r"Period:\s*(.*?)\s+(?:To|to)\s+(.*)",
            text
        )

        if period_match and len(period_match.groups()) >= 2:
            period_start = period_match.group(1).strip()
            period_end = period_match.group(2).strip()

        gstin_matches = re.findall(
            r"GSTIN[:\s]+([0-9A-Z]{15})",
            text
        )

        company_gstin = gstin_matches[0] if len(gstin_matches) > 0 else ""
        merchant_gstin = gstin_matches[1] if len(gstin_matches) > 1 else ""

        particular = ""
        particular_amount = 0.0

        for line in lines:
            match = re.match(
                r"^\d+\s+(.*?)\s+([\d,]+\.\d+)$",
                line
            )
            if match:
                particular = match.group(1).strip()
                particular_amount = to_float(match.group(2))
                break

        taxable_amount = to_float(extract(r"Taxable Amount\s+([\d,]+\.\d+)", text))
        
        sgst_rate = to_float(extract(r"SGST\s*@\s*([0-9.]+)", text))
        sgst_amount = to_float(extract(r"SGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

        cgst_rate = to_float(extract(r"CGST\s*@\s*([0-9.]+)", text))
        cgst_amount = to_float(extract(r"CGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

        igst_rate = to_float(extract(r"IGST\s*@\s*([0-9.]+)", text))
        igst_amount = to_float(extract(r"IGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

        total_amount = to_float(extract(r"Total Amount\s+([\d,]+\.\d+)", text))

        return {
            "File Name": os.path.basename(pdf_path),
            "Invoice No": invoice_no,
            "Invoice Date": invoice_date,
            "Period Start": period_start,
            "Period End": period_end,
            "Merchant Name": merchant_name,
            "Company GSTIN": company_gstin,
            "Merchant GSTIN": merchant_gstin,
            "HSN Code": hsn_code,
            "Service Description": service_desc,
            "Particular": particular,
            "Particular Amount": particular_amount,
            "Taxable Amount": taxable_amount,
            "SGST Rate (%)": sgst_rate,
            "SGST Amount": sgst_amount,
            "CGST Rate (%)": cgst_rate,
            "CGST Amount": cgst_amount,
            "IGST Rate (%)": igst_rate,
            "IGST Amount": igst_amount,
            "Total Amount": total_amount
        }

    except Exception as e:
        return {
            "File Name": os.path.basename(pdf_path),
            "Error": str(e)
        }


# ============================================
# API FUNCTION CALLED BY app.py
# ============================================

async def upload_flipkart(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = None
):
    files_count = len(files)
    temp_paths = []

    try:
        # Stream chunks to temp file rather than loading entire payload in RAM
        for file in files:
            tmp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            )
            try:
                shutil.copyfileobj(file.file, tmp)
            finally:
                tmp.close()
                file.file.close()
            temp_paths.append(tmp.name)

        # Sequential processing with explicit memory garbage collection
        data = []
        for path in temp_paths:
            res = process_pdf(path)
            if res:
                data.append(res)
            gc.collect()  # Force instant memory recovery

        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file = f"flipkart_invoice_details_{timestamp}.xlsx"

        df.to_excel(excel_file, index=False)
        
        # Log to database safely if user context exists
        if files_count > 0 and current_user and hasattr(current_user, 'id'):
            analytics = UploadAnalytics(
                user_id=current_user.id,
                source="flipkart",
                pdf_count=files_count
            )
            db.add(analytics)
            db.commit()

        # Schedule excel file cleanup after download
        background_tasks.add_task(remove_file, excel_file)

        return FileResponse(
            path=excel_file,
            filename=excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    finally:
        # Safely clean up temporary PDFs
        for path in temp_paths:
            remove_file(path)
        gc.collect()