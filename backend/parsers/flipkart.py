from fastapi import UploadFile, File
from fastapi.responses import FileResponse
 
import fitz
import pandas as pd
import re
import os
import uuid
 
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
# ---------------------------
# HELPERS
# ---------------------------
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
 
 
# ---------------------------
# MAIN API
# ---------------------------
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
 
        # ---------------------------
        # COMMON FIELDS
        # ---------------------------
        company_name = extract(r'BILLED FROM:\s*(.*?)\s*(?:Tel:|GSTIN:|CIN:)', text)
        company_gstin = extract(r'BILLED FROM:.*?GSTIN:\s*([A-Z0-9]{15})', text)
        customer_name = extract(r'Business Name:\s*(.*?)\s*Address:', text)
        customer_gstin = extract(r'BILLED TO:.*?GSTIN:\s*([A-Z0-9]{15})', text)
 
        invoice_no = extract(r'Invoice\s*#:\s*([A-Z0-9\-\/]+)', text)
        invoice_date = extract(r'Invoice Date:\s*([0-9\-\/]+)', text)
 
        is_credit_note = "Credit Note" in text
 
        # ===================================================
        # ✅ CREDIT NOTE
        # ===================================================
        if is_credit_note:
 
            credit_no = extract(r'Credit Note\s*#:\s*([A-Z0-9\-\/]+)', text)
            credit_date = extract(r'Credit Note Date:\s*([0-9\-\/]+)', text)
            description = extract(r'Particulars:\s*(.*?)\s*BILLED TO:', text)
 
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
                "CGST Rate": "",
                "CGST Amount": "",
                "SGST Rate": "",
                "SGST Amount": "",
                "Line Total": "",
                "Invoice Total": "",
                "Credit Note No": credit_no,
                "Credit Note Date": credit_date,
                "Amount": amount
            })
 
        # ===================================================
        # ✅ INVOICE
        # ===================================================
        else:
 
            # Detect tax type correctly
            has_cgst = "CGST Rate" in text and "SGST Rate" in text
            has_igst = "IGST Rate" in text
 
            # ✅ FIXED invoice total extraction
            invoice_total_match = re.search(
                r'Total\s+[0-9,]+\.\d+\s+[0-9,]+\.\d+\s+[0-9,]+\.\d+\s+([0-9,]+\.\d+)',
                text
            )
            invoice_total = clean_number(invoice_total_match.group(1)) if invoice_total_match else 0.0
 
            # ---------------------------------
            # ✅ CGST + SGST (ONLY)
            # ---------------------------------
            if has_cgst:
 
                cgst_pattern = re.compile(
                    r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
                    re.IGNORECASE
                )
 
                rows = cgst_pattern.findall(text)
 
                for row in rows:
                    sac, desc, taxable, cgst_rate, sgst_rate, cgst_amt, sgst_amt = row
 
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
 
                        "IGST Rate": 0,
                        "IGST Amount": 0,
 
                        "CGST Rate": clean_number(cgst_rate),
                        "CGST Amount": clean_number(cgst_amt),
                        "SGST Rate": clean_number(sgst_rate),
                        "SGST Amount": clean_number(sgst_amt),
 
                        "Line Total": (
                            clean_number(taxable)
                            + clean_number(cgst_amt)
                            + clean_number(sgst_amt)
                        ),
 
                        "Invoice Total": invoice_total,
 
                        "Credit Note No": "",
                        "Credit Note Date": "",
                        "Amount": ""
                    })
 
            # ---------------------------------
            # ✅ IGST ONLY
            # ---------------------------------
            elif has_igst:
 
                igst_pattern = re.compile(
                    r'(\d{6})\s+(.*?)\s+([0-9,]+\.\d+)\s+([0-9.]+)\s+([0-9,]+\.\d+)\s+([0-9,]+\.\d+)',
                    re.IGNORECASE
                )
 
                rows = igst_pattern.findall(text)
 
                for row in rows:
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
 
                        "CGST Rate": 0,
                        "CGST Amount": 0,
                        "SGST Rate": 0,
                        "SGST Amount": 0,
 
                        "Line Total": clean_number(total),
                        "Invoice Total": invoice_total,
 
                        "Credit Note No": "",
                        "Credit Note Date": "",
                        "Amount": ""
                    })
 
    # ---------------------------
    # FINAL DATAFRAME
    # ---------------------------
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
        "CGST Rate",
        "CGST Amount",
        "SGST Rate",
        "SGST Amount",
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