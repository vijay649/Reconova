import os
import re
import shutil
from typing import List
import fitz
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openpyxl import load_workbook
from sqlalchemy.orm import Session

# Agar database use kar rahe hain toh dependencies import karein, nahi toh dummy session use hoga
from database.database import get_db
from database.models import User, UploadAnalytics

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = FastAPI()

# Frontend dashboard errors se bachne ke liye CORS enabled rakhein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_text(text):
    if text is None:
        return ""
    text = text.replace("\n", " ")
    return re.sub(r"\s+", " ", text).strip()

def clean_number(value):
    if not value:
        return 0.0
    value = str(value).replace("INR", "").replace("-INR", "-").replace(",", "").strip()
    try:
        return float(value)
    except Exception:
        return 0.0

def extract(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""

# =====================================================
# FIX: FRONTEND DASHBOARD ERRORS (404 FIXES)
# =====================================================

@app.get("/admin/total-users")
def get_total_users():
    # Frontend ko data dene ke liye dummy response (Isko aap DB query se replace kar sakte hain)
    return {"total_users": 9}

@app.get("/admin/verified-users")
def get_verified_users():
    return {"verified_users": 9}

@app.get("/admin/total-uploads")
def get_total_uploads():
    return {"total_uploads": 137}


# =====================================================
# MAIN UPLOAD & PARSER API
# =====================================================
@app.post("/upload-amazon")
async def upload_amazon(files: List[UploadFile] = File(...)):
    results = []

    for file in files:  
        try:
            if not file.filename.lower().endswith('.pdf'):
                continue

            safe_filename = os.path.basename(file.filename).replace("/", "_").replace("\\", "_")
            save_path = os.path.join(UPLOAD_FOLDER, safe_filename)

            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            doc = fitz.open(save_path)
            full_text = "".join([page.get_text() for page in doc])
            doc.close()

            normalized_text = clean_text(full_text).split("Details of Fees to the above")[0]

            document_type = "Credit Note" if "Credit Note" in normalized_text else "Invoice"

            company_name = extract(r"(Amazon Seller Services Private Limited|Amazon Retail India Private Limited)", normalized_text)
            company_gstin = extract(r"GST Tax Registration No:\s*([A-Z0-9]+)", normalized_text)
            invoice_no = extract(r"(?:Invoice Number|Credit Note Number)\s*:\s*([A-Z0-9\-]+)", normalized_text)
            invoice_date = extract(r"(?:Invoice Date|Credit Note Date)\s*:\s*([0-9\/\-]+)", normalized_text)
            invoice_total = clean_number(extract(r"Total(?: Invoice amount)?\s*:?\s*INR\s*([0-9,]+\.\d+)", normalized_text))

            customer_name = extract(r"Bill to\s*Name:\s*(.*?)Address:", normalized_text)
            customer_gstin = extract(r"GSTIN:\s*([A-Z0-9]+)", normalized_text)

            if document_type == "Invoice":
                row_pattern = re.compile(r"(\d+)\.\s+(\d{6})\s+(.*?)\s+INR\s*([0-9,]+\.\d+)(.*?)(?=\d+\.\s+\d{6}|\Z)", re.IGNORECASE | re.DOTALL)
                matches = row_pattern.findall(normalized_text)

                for row in matches:
                    serial_no, sac_code, description, fee_str, tax_text = row
                    fee_amount = clean_number(fee_str)

                    sgst_rate, sgst_amount = 0.0, 0.0
                    cgst_rate, cgst_amount = 0.0, 0.0
                    igst_rate, igst_amount = 0.0, 0.0

                    sgst_match = re.search(r"SGST\s*([0-9\.]+)%\s*INR\s*([0-9,]+\.\d+)", tax_text)
                    if sgst_match:
                        sgst_rate = clean_number(sgst_match.group(1))
                        sgst_amount = clean_number(sgst_match.group(2))

                    cgst_match = re.search(r"CGST\s*([0-9\.]+)%\s*INR\s*([0-9,]+\.\d+)", tax_text)
                    if cgst_match:
                        cgst_rate = clean_number(cgst_match.group(1))
                        cgst_amount = clean_number(cgst_match.group(2))

                    igst_match = re.search(r"IGST\s*([0-9\.]+)%\s*INR\s*([0-9,]+\.\d+)", tax_text)
                    if igst_match:
                        igst_rate = clean_number(igst_match.group(1))
                        igst_amount = clean_number(igst_match.group(2))

                    line_total = round(fee_amount + sgst_amount + cgst_amount + igst_amount, 2)

                    results.append({
                        "File Name": safe_filename, "Document Type": document_type, "Invoice No": invoice_no, "Invoice Date": invoice_date,
                        "Original Invoice No": "", "Original Invoice Date": "", "Company Name": company_name, "Company GSTIN": company_gstin,
                        "Customer Name": customer_name, "Customer GSTIN": customer_gstin, "SAC Code": sac_code, "Description": clean_text(description),
                        "Fee Amount": fee_amount, "SGST Rate": sgst_rate, "SGST Amount": sgst_amount, "CGST Rate": cgst_rate, "CGST Amount": cgst_amount,
                        "IGST Rate": igst_rate, "IGST Amount": igst_amount, "Line Total": line_total, "Invoice Total": invoice_total
                    })

            else:
                # =====================================================
                # FIXED CREDIT NOTE LOGIC WITH AUTO TAX CALCULATION
                # =====================================================
                credit_pattern = re.compile(r"(\d+)\.\s*([A-Z0-9\-]+)\s*([0-9\-]+)\s*(\d{6})\s*(.*?)\s*INR\s*([0-9,]+\.\d+)", re.IGNORECASE | re.DOTALL)
                credit_matches = credit_pattern.findall(normalized_text)

                for item in credit_matches:
                    serial_no, orig_inv, orig_date, sac_code, description, amount_str = item
                    fee_amount = -abs(clean_number(amount_str))

                    # Reverse Calculation: Agar customer aur company ka GST state match karta hai toh CGST+SGST, nahi toh IGST
                    # Standard Amazon seller fee par 18% GST lagta hai
                    is_interstate = company_gstin[:2] != customer_gstin[:2] if (company_gstin and customer_gstin) else False

                    if is_interstate:
                        igst_rate = 18.0
                        igst_amount = round(fee_amount * 0.18, 2)
                        cgst_rate = cgst_amount = sgst_rate = sgst_amount = 0.0
                    else:
                        cgst_rate = 9.0
                        cgst_amount = round(fee_amount * 0.09, 2)
                        sgst_rate = 9.0
                        sgst_amount = round(fee_amount * 0.09, 2)
                        igst_rate = igst_amount = 0.0

                    line_total = round(fee_amount + sgst_amount + cgst_amount + igst_amount, 2)

                    results.append({
                        "File Name": safe_filename, "Document Type": "Credit Note", "Invoice No": invoice_no, "Invoice Date": invoice_date,
                        "Original Invoice No": orig_inv, "Original Invoice Date": orig_date, "Company Name": company_name, "Company GSTIN": company_gstin,
                        "Customer Name": customer_name, "Customer GSTIN": customer_gstin, "SAC Code": sac_code, "Description": clean_text(description),
                        "Fee Amount": fee_amount, "SGST Rate": sgst_rate, "SGST Amount": sgst_amount, "CGST Rate": cgst_rate, "CGST Amount": cgst_amount,
                        "IGST Rate": igst_rate, "IGST Amount": igst_amount, "Line Total": line_total, "Invoice Total": -abs(invoice_total)
                    })

        except Exception as e:
            print(f"ERROR PROCESSING FILE {file.filename}: {str(e)}")

    df = pd.DataFrame(results)
    if df.empty:
        df = pd.DataFrame([{"Message": "No Data Found"}])

    output_file = os.path.join(OUTPUT_FOLDER, "Amazon_Invoice_Output.xlsx")
    if os.path.exists(output_file):
        os.remove(output_file)

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Invoices")

    # Column Formatting
    wb = load_workbook(output_file)
    ws = wb.active
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 5
    wb.save(output_file)
    wb.close()

    return FileResponse(
        path=output_file,
        filename="Amazon_Invoice_Output.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="Amazon_Invoice_Output.xlsx"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )