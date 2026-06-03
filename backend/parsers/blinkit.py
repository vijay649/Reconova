# # ============================================
# # BLINKIT GST INVOICE EXTRACTOR
# # ============================================

# # pip install pdfplumber pandas openpyxl

# import pdfplumber
# import pandas as pd
# import re
# import os

# from glob import glob
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor

# # ============================================
# # FOLDER
# # ============================================

# PDF_FOLDER = r"D:\Blinkit_Invoices\Blinkit_Exp"

# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# OUTPUT_FILE = os.path.join(
#     PDF_FOLDER,
#     f"blinkit_invoice_details_{timestamp}.xlsx"
# )

# # ============================================
# # PDF FILES
# # ============================================

# pdf_files = glob(
#     os.path.join(PDF_FOLDER, "*.pdf")
# )

# print(f"\nFound {len(pdf_files)} PDF files\n")

# # ============================================
# # HELPERS
# # ============================================

# def extract(pattern, text):

#     match = re.search(
#         pattern,
#         text,
#         re.IGNORECASE | re.DOTALL
#     )

#     return match.group(1).strip() if match else ""


# def to_float(value):

#     if not value:
#         return 0.0

#     try:
#         return float(
#             value.replace(",", "").strip()
#         )
#     except:
#         return 0.0


# # ============================================
# # PROCESS SINGLE PDF
# # ============================================

# def process_pdf(pdf_file):

#     try:

#         with pdfplumber.open(pdf_file) as pdf:

#             text = pdf.pages[0].extract_text() or ""

#         lines = [
#             line.strip()
#             for line in text.split("\n")
#             if line.strip()
#         ]

#         # ====================================
#         # BASIC DETAILS
#         # ====================================

#         invoice_no = extract(
#             r"Invoice No[:\s]+([A-Z0-9\-]+)",
#             text
#         )

#         invoice_date = extract(
#             r"Invoice Date[:\s]+([0-9\-]+)",
#             text
#         )

#         merchant_name = extract(
#             r"Entity Name[:\s]+(.*?)\s+State",
#             text
#         )

#         hsn_code = extract(
#             r"HSN Code[:\s]+(\d+)",
#             text
#         )

#         service_desc = extract(
#             r"Service Description[:\s]+(.*?)\s+Work Description",
#             text
#         )

#         # ====================================
#         # PERIOD
#         # ====================================

#         period_start = ""
#         period_end = ""

#         period_match = re.search(
#             r"Period:\s*(.*?)\s+(?:To|to)\s+(.*)",
#             text
#         )

#         if period_match:

#             period_start = period_match.group(1).strip()

#             period_end = period_match.group(2).strip()

#         # ====================================
#         # GSTIN
#         # ====================================

#         gstin_matches = re.findall(
#             r"GSTIN[:\s]+([0-9A-Z]{15})",
#             text
#         )

#         company_gstin = (
#             gstin_matches[0]
#             if len(gstin_matches) > 0
#             else ""
#         )

#         merchant_gstin = (
#             gstin_matches[1]
#             if len(gstin_matches) > 1
#             else ""
#         )

#         # ====================================
#         # PARTICULAR ROW
#         # ====================================

#         particular = ""
#         particular_amount = 0.0

#         for line in lines:

#             match = re.match(
#                 r"^\d+\s+(.*?)\s+([\d,]+\.\d+)$",
#                 line
#             )

#             if match:

#                 particular = match.group(1).strip()

#                 particular_amount = to_float(
#                     match.group(2)
#                 )

#                 break

#         # ====================================
#         # TAX DETAILS
#         # ====================================

#         taxable_amount = to_float(
#             extract(
#                 r"Taxable Amount\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         sgst_rate = to_float(
#             extract(
#                 r"SGST\s*@\s*([0-9.]+)",
#                 text
#             )
#         )

#         sgst_amount = to_float(
#             extract(
#                 r"SGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         cgst_rate = to_float(
#             extract(
#                 r"CGST\s*@\s*([0-9.]+)",
#                 text
#             )
#         )

#         cgst_amount = to_float(
#             extract(
#                 r"CGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         igst_rate = to_float(
#             extract(
#                 r"IGST\s*@\s*([0-9.]+)",
#                 text
#             )
#         )

#         igst_amount = to_float(
#             extract(
#                 r"IGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         total_amount = to_float(
#             extract(
#                 r"Total Amount\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         # ====================================
#         # RETURN ROW
#         # ====================================

#         return [{

#             "File Name": os.path.basename(pdf_file),

#             "Invoice No": invoice_no,
#             "Invoice Date": invoice_date,

#             "Period Start": period_start,
#             "Period End": period_end,

#             "Merchant Name": merchant_name,

#             "Company GSTIN": company_gstin,
#             "Merchant GSTIN": merchant_gstin,

#             "HSN Code": hsn_code,
#             "Service Description": service_desc,

#             "Particular": particular,
#             "Particular Amount": particular_amount,

#             "Taxable Amount": taxable_amount,

#             "SGST Rate (%)": sgst_rate,
#             "SGST Amount": sgst_amount,

#             "CGST Rate (%)": cgst_rate,
#             "CGST Amount": cgst_amount,

#             "IGST Rate (%)": igst_rate,
#             "IGST Amount": igst_amount,

#             "Total Amount": total_amount

#         }]

#     except Exception as e:

#         print(
#             f"Error processing "
#             f"{os.path.basename(pdf_file)}"
#         )

#         print(str(e))

#         return []


# # ============================================
# # MULTITHREADING
# # ============================================

# all_data = []

# with ThreadPoolExecutor(max_workers=8) as executor:

#     results = executor.map(
#         process_pdf,
#         pdf_files
#     )

#     for result in results:

#         all_data.extend(result)

# # ============================================
# # DATAFRAME
# # ============================================

# df = pd.DataFrame(all_data)

# # ============================================
# # SAVE EXCEL
# # ============================================

# df.to_excel(
#     OUTPUT_FILE,
#     index=False
# )

# # ============================================
# # COMPLETE
# # ============================================

# print("\n================================")
# print("DONE")
# print("================================")

# print(f"\nSaved File:\n{OUTPUT_FILE}")
# print(f"\nTotal Rows: {len(df)}")






# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import FileResponse

# from typing import List

# import pdfplumber
# import pandas as pd
# import re
# import os
# import shutil
# import uuid

# from concurrent.futures import ThreadPoolExecutor

# # app = FastAPI()

# # ============================================
# # FOLDERS
# # ============================================

# UPLOAD_DIR = "uploads"
# OUTPUT_DIR = "output"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ============================================
# # HELPERS
# # ============================================

# def extract(pattern, text):

#     match = re.search(
#         pattern,
#         text,
#         re.IGNORECASE | re.DOTALL
#     )

#     return match.group(1).strip() if match else ""


# def to_float(value):

#     if not value:
#         return 0.0

#     try:

#         return float(
#             str(value)
#             .replace(",", "")
#             .strip()
#         )

#     except:

#         return 0.0


# # ============================================
# # PROCESS SINGLE PDF
# # ============================================

# def process_pdf(pdf_file):

#     try:

#         with pdfplumber.open(pdf_file) as pdf:

#             text = pdf.pages[0].extract_text() or ""

#         lines = [

#             line.strip()

#             for line in text.split("\n")

#             if line.strip()

#         ]

#         # ====================================
#         # BASIC DETAILS
#         # ====================================

#         invoice_no = extract(
#             r"Invoice No[:\s]+([A-Z0-9\-]+)",
#             text
#         )

#         invoice_date = extract(
#             r"Invoice Date[:\s]+([0-9\-]+)",
#             text
#         )

#         merchant_name = extract(
#             r"Entity Name[:\s]+(.*?)\s+State",
#             text
#         )

#         hsn_code = extract(
#             r"HSN Code[:\s]+(\d+)",
#             text
#         )

#         service_desc = extract(
#             r"Service Description[:\s]+(.*?)\s+Work Description",
#             text
#         )

#         # ====================================
#         # PERIOD
#         # ====================================

#         period_start = ""
#         period_end = ""

#         period_match = re.search(
#             r"Period:\s*(.*?)\s+(?:To|to)\s+(.*)",
#             text
#         )

#         if period_match:

#             period_start = (
#                 period_match.group(1)
#                 .strip()
#             )

#             period_end = (
#                 period_match.group(2)
#                 .strip()
#             )

#         # ====================================
#         # GSTIN
#         # ====================================

#         gstin_matches = re.findall(
#             r"GSTIN[:\s]+([0-9A-Z]{15})",
#             text
#         )

#         company_gstin = (

#             gstin_matches[0]

#             if len(gstin_matches) > 0

#             else ""

#         )

#         merchant_gstin = (

#             gstin_matches[1]

#             if len(gstin_matches) > 1

#             else ""

#         )

#         # ====================================
#         # PARTICULAR ROW
#         # ====================================

#         particular = ""
#         particular_amount = 0.0

#         for line in lines:

#             match = re.match(
#                 r"^\d+\s+(.*?)\s+([\d,]+\.\d+)$",
#                 line
#             )

#             if match:

#                 particular = (
#                     match.group(1)
#                     .strip()
#                 )

#                 particular_amount = to_float(
#                     match.group(2)
#                 )

#                 break

#         # ====================================
#         # TAX DETAILS
#         # ====================================

#         taxable_amount = to_float(
#             extract(
#                 r"Taxable Amount\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         sgst_rate = to_float(
#             extract(
#                 r"SGST\s*@\s*([0-9.]+)",
#                 text
#             )
#         )

#         sgst_amount = to_float(
#             extract(
#                 r"SGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         cgst_rate = to_float(
#             extract(
#                 r"CGST\s*@\s*([0-9.]+)",
#                 text
#             )
#         )

#         cgst_amount = to_float(
#             extract(
#                 r"CGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         igst_rate = to_float(
#             extract(
#                 r"IGST\s*@\s*([0-9.]+)",
#                 text
#             )
#         )

#         igst_amount = to_float(
#             extract(
#                 r"IGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         total_amount = to_float(
#             extract(
#                 r"Total Amount\s+([\d,]+\.\d+)",
#                 text
#             )
#         )

#         return [{

#             "File Name":
#                 os.path.basename(pdf_file),

#             "Invoice No":
#                 invoice_no,

#             "Invoice Date":
#                 invoice_date,

#             "Period Start":
#                 period_start,

#             "Period End":
#                 period_end,

#             "Merchant Name":
#                 merchant_name,

#             "Company GSTIN":
#                 company_gstin,

#             "Merchant GSTIN":
#                 merchant_gstin,

#             "HSN Code":
#                 hsn_code,

#             "Service Description":
#                 service_desc,

#             "Particular":
#                 particular,

#             "Particular Amount":
#                 particular_amount,

#             "Taxable Amount":
#                 taxable_amount,

#             "SGST Rate (%)":
#                 sgst_rate,

#             "SGST Amount":
#                 sgst_amount,

#             "CGST Rate (%)":
#                 cgst_rate,

#             "CGST Amount":
#                 cgst_amount,

#             "IGST Rate (%)":
#                 igst_rate,

#             "IGST Amount":
#                 igst_amount,

#             "Total Amount":
#                 total_amount

#         }]

#     except Exception as e:

#         print(
#             f"Error processing "
#             f"{os.path.basename(pdf_file)}"
#         )

#         print(str(e))

#         return []


# # ============================================
# # API
# # ============================================

# # @app.post("/upload-blinkit")
# async def upload_blinkit(
#     files: List[UploadFile] = File(...)
# ):

#     request_id = str(uuid.uuid4())

#     upload_folder = os.path.join(
#         UPLOAD_DIR,
#         request_id
#     )

#     os.makedirs(
#         upload_folder,
#         exist_ok=True
#     )

#     saved_files = []

#     # ========================================
#     # SAVE FILES
#     # ========================================

#     # for file in files:

#     #     filename = os.path.basename(file.filename)

#     #     file_path = os.path.join(
#     #         upload_folder,
#     #         filename
#     #     )


#     #     # file_path = os.path.join(
#     #     #     upload_folder,
#     #     #     file.filename
#     #     # )

#     #     with open(
#     #         file_path,
#     #         "wb"
#     #     ) as buffer:

#     #         shutil.copyfileobj(
#     #             file.file,
#     #             buffer
#     #         )

#     #     saved_files.append(
#     #         file_path
#     #     )

#     for file in files:

#     # Folder path hata kar sirf PDF ka naam lo
#         filename = file.filename.replace("\\", "/").split("/")[-1]

#         file_path = os.path.join(
#             upload_folder,
#             filename
#         )

#         print(f"Original filename: {file.filename}")
#         print(f"Saving file to: {file_path}")

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(
#                 file.file,
#                 buffer
#             )

#         saved_files.append(file_path)


#     # ========================================
#     # MULTITHREADING
#     # ========================================

#     all_data = []

#     with ThreadPoolExecutor(
#         max_workers=8
#     ) as executor:

#         results = executor.map(
#             process_pdf,
#             saved_files
#         )

#         for result in results:

#             all_data.extend(
#                 result
#             )

#     # ========================================
#     # DATAFRAME
#     # ========================================

#     df = pd.DataFrame(
#         all_data
#     )

#     # ========================================
#     # EXCEL
#     # ========================================

#     output_file = os.path.join(
#         OUTPUT_DIR,
#         f"blinkit_invoice_details_{request_id}.xlsx"
#     )

#     df.to_excel(
#         output_file,
#         index=False
#     )

#     # ========================================
#     # RETURN FILE
#     # ========================================

#     return FileResponse(
#         path=output_file,
#         filename="blinkit_invoice_details.xlsx",
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )



from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from concurrent.futures import ThreadPoolExecutor
 
import pdfplumber
import pandas as pd
import tempfile
import re
import os
from datetime import datetime
 
 
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
    except:
        return 0.0
 
 
# ============================================
# PROCESS PDF
# ============================================
 
def process_pdf(pdf_path):
 
    try:
 
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text() or ""
 
        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]
 
        invoice_no = extract(
            r"Invoice No[:\s]+([A-Z0-9\-]+)",
            text
        )
 
        invoice_date = extract(
            r"Invoice Date[:\s]+([0-9\-]+)",
            text
        )
 
        merchant_name = extract(
            r"Entity Name[:\s]+(.*?)\s+State",
            text
        )
 
        hsn_code = extract(
            r"HSN Code[:\s]+(\d+)",
            text
        )
 
        service_desc = extract(
            r"Service Description[:\s]+(.*?)\s+Work Description",
            text
        )
 
        period_start = ""
        period_end = ""
 
        period_match = re.search(
            r"Period:\s*(.*?)\s+(?:To|to)\s+(.*)",
            text
        )
 
        if period_match:
            period_start = period_match.group(1).strip()
            period_end = period_match.group(2).strip()
 
        gstin_matches = re.findall(
            r"GSTIN[:\s]+([0-9A-Z]{15})",
            text
        )
 
        company_gstin = (
            gstin_matches[0]
            if len(gstin_matches) > 0
            else ""
        )
 
        merchant_gstin = (
            gstin_matches[1]
            if len(gstin_matches) > 1
            else ""
        )
 
        particular = ""
        particular_amount = 0.0
 
        for line in lines:
 
            match = re.match(
                r"^\d+\s+(.*?)\s+([\d,]+\.\d+)$",
                line
            )
 
            if match:
 
                particular = match.group(1).strip()
 
                particular_amount = to_float(
                    match.group(2)
                )
 
                break
 
        taxable_amount = to_float(
            extract(
                r"Taxable Amount\s+([\d,]+\.\d+)",
                text
            )
        )
 
        sgst_rate = to_float(
            extract(
                r"SGST\s*@\s*([0-9.]+)",
                text
            )
        )
 
        sgst_amount = to_float(
            extract(
                r"SGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
                text
            )
        )
 
        cgst_rate = to_float(
            extract(
                r"CGST\s*@\s*([0-9.]+)",
                text
            )
        )
 
        cgst_amount = to_float(
            extract(
                r"CGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
                text
            )
        )
 
        igst_rate = to_float(
            extract(
                r"IGST\s*@\s*([0-9.]+)",
                text
            )
        )
 
        igst_amount = to_float(
            extract(
                r"IGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)",
                text
            )
        )
 
        total_amount = to_float(
            extract(
                r"Total Amount\s+([\d,]+\.\d+)",
                text
            )
        )
 
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
 
async def upload_blinkit(
    files: list[UploadFile] = File(...)
):
 
    temp_paths = []
 
    try:
 
        for file in files:
 
            tmp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            )
 
            content = await file.read()
 
            tmp.write(content)
            tmp.close()
 
            temp_paths.append(tmp.name)
 
        with ThreadPoolExecutor(
            max_workers=8
        ) as executor:
 
            data = list(
                executor.map(
                    process_pdf,
                    temp_paths
                )
            )
 
        df = pd.DataFrame(data)
 
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
 
        excel_file = (
            f"blinkit_invoice_details_"
            f"{timestamp}.xlsx"
        )
 
        df.to_excel(
            excel_file,
            index=False
        )
 
        return FileResponse(
            path=excel_file,
            filename=excel_file,
            media_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )
 
    finally:
 
        for path in temp_paths:
 
            try:
                os.remove(path)
            except:
                pass