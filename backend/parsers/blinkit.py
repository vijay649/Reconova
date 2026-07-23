# from fastapi import Depends

# from sqlalchemy.orm import Session

# from auth.dependencies import get_current_user

# from database.database import get_db

# from database.models import UploadAnalytics, User



# from fastapi import UploadFile, File
# from fastapi.responses import FileResponse
# from concurrent.futures import ThreadPoolExecutor
 
# import pdfplumber
# import pandas as pd
# import tempfile
# import re
# import os
# from datetime import datetime
 
 
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
# # PROCESS PDF
# # ============================================
 
# def process_pdf(pdf_path):
 
#     try:
 
#         with pdfplumber.open(pdf_path) as pdf:
#             text = pdf.pages[0].extract_text() or ""
 
#         lines = [
#             line.strip()
#             for line in text.split("\n")
#             if line.strip()
#         ]
 
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
 
#         period_start = ""
#         period_end = ""
 
#         period_match = re.search(
#             r"Period:\s*(.*?)\s+(?:To|to)\s+(.*)",
#             text
#         )
 
#         if period_match:
#             period_start = period_match.group(1).strip()
#             period_end = period_match.group(2).strip()
 
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
 
#         return {
#             "File Name": os.path.basename(pdf_path),
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
#         }
 
#     except Exception as e:
 
#         return {
#             "File Name": os.path.basename(pdf_path),
#             "Error": str(e)
#         }
 
 
# # ============================================
# # API FUNCTION CALLED BY app.py
# # ============================================
 
# async def upload_blinkit(
#     files: list[UploadFile] = File(...),
#      db: Session = Depends(get_db),

#     current_user: User = Depends(
#         get_current_user
#     )
# ):
#     files_count = len(files)
 
#     temp_paths = []
 
#     try:
 
#         for file in files:
 
#             tmp = tempfile.NamedTemporaryFile(
#                 delete=False,
#                 suffix=".pdf"
#             )
 
#             content = await file.read()
 
#             tmp.write(content)
#             tmp.close()
 
#             temp_paths.append(tmp.name)
 
#         with ThreadPoolExecutor(
#             max_workers=8
#         ) as executor:
 
#             data = list(
#                 executor.map(
#                     process_pdf,
#                     temp_paths
#                 )
#             )
 
#         df = pd.DataFrame(data)
 
#         timestamp = datetime.now().strftime(
#             "%Y%m%d_%H%M%S"
#         )
 
#         excel_file = (
#             f"blinkit_invoice_details_"
#             f"{timestamp}.xlsx"
#         )
 
#         df.to_excel(
#             excel_file,
#             index=False
#         )
        
#         if files_count > 0:
        
#             analytics = UploadAnalytics(

#                 user_id=current_user.id,

#                 source="blinkit",

#                 pdf_count=files_count
#             )

#             db.add(analytics)

#             db.commit()
 
#         return FileResponse(
#             path=excel_file,
#             filename=excel_file,
#             media_type=(
#                 "application/vnd.openxmlformats-"
#                 "officedocument.spreadsheetml.sheet"
#             )
#         )
 
#     finally:
 
#         for path in temp_paths:
 
#             try:
#                 os.remove(path)
#             except:
#                 pass


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# import os
# import re
# import tempfile
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor

# import pdfplumber
# import pandas as pd
# from fastapi import Depends, UploadFile, File, BackgroundTasks
# from fastapi.responses import FileResponse
# from sqlalchemy.orm import Session

# from auth.dependencies import get_current_user
# from database.database import get_db
# from database.models import UploadAnalytics, User


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


# def remove_file(path: str):
#     """Callback function to safely delete files after response delivery"""
#     try:
#         if os.path.exists(path):
#             os.remove(path)
#     except Exception:
#         pass


# # ============================================
# # PROCESS PDF
# # ============================================

# def process_pdf(pdf_path):
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             if not pdf.pages:
#                 return {"File Name": os.path.basename(pdf_path), "Error": "PDF is empty"}
#             text = pdf.pages[0].extract_text() or ""

#         lines = [
#             line.strip()
#             for line in text.split("\n")
#             if line.strip()
#         ]

#         invoice_no = extract(r"Invoice No[:\s]+([A-Z0-9\-]+)", text)
#         invoice_date = extract(r"Invoice Date[:\s]+([0-9\-]+)", text)
#         merchant_name = extract(r"Entity Name[:\s]+(.*?)\s+State", text)
#         hsn_code = extract(r"HSN Code[:\s]+(\d+)", text)
#         service_desc = extract(r"Service Description[:\s]+(.*?)\s+Work Description", text)

#         period_start = ""
#         period_end = ""

#         period_match = re.search(
#             r"Period:\s*(.*?)\s+(?:To|to)\s+(.*)",
#             text
#         )

#         if period_match and len(period_match.groups()) >= 2:
#             period_start = period_match.group(1).strip()
#             period_end = period_match.group(2).strip()

#         gstin_matches = re.findall(
#             r"GSTIN[:\s]+([0-9A-Z]{15})",
#             text
#         )

#         company_gstin = gstin_matches[0] if len(gstin_matches) > 0 else ""
#         merchant_gstin = gstin_matches[1] if len(gstin_matches) > 1 else ""

#         particular = ""
#         particular_amount = 0.0

#         for line in lines:
#             match = re.match(
#                 r"^\d+\s+(.*?)\s+([\d,]+\.\d+)$",
#                 line
#             )
#             if match:
#                 particular = match.group(1).strip()
#                 particular_amount = to_float(match.group(2))
#                 break

#         taxable_amount = to_float(extract(r"Taxable Amount\s+([\d,]+\.\d+)", text))
        
#         sgst_rate = to_float(extract(r"SGST\s*@\s*([0-9.]+)", text))
#         sgst_amount = to_float(extract(r"SGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

#         cgst_rate = to_float(extract(r"CGST\s*@\s*([0-9.]+)", text))
#         cgst_amount = to_float(extract(r"CGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

#         igst_rate = to_float(extract(r"IGST\s*@\s*([0-9.]+)", text))
#         igst_amount = to_float(extract(r"IGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

#         total_amount = to_float(extract(r"Total Amount\s+([\d,]+\.\d+)", text))

#         return {
#             "File Name": os.path.basename(pdf_path),
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
#         }

#     except Exception as e:
#         return {
#             "File Name": os.path.basename(pdf_path),
#             "Error": str(e)
#         }


# # ============================================
# # API FUNCTION CALLED BY app.py
# # ============================================

# async def upload_blinkit(
#     background_tasks: BackgroundTasks,
#     files: list[UploadFile] = File(...),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     files_count = len(files)
#     temp_paths = []

#     try:
#         for file in files:
#             tmp = tempfile.NamedTemporaryFile(
#                 delete=False,
#                 suffix=".pdf"
#             )
#             content = await file.read()
#             tmp.write(content)
#             tmp.close()
#             temp_paths.append(tmp.name)

#         with ThreadPoolExecutor(max_workers=8) as executor:
#             data = list(
#                 executor.map(
#                     process_pdf,
#                     temp_paths
#                 )
#             )

#         df = pd.DataFrame(data)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         excel_file = f"blinkit_invoice_details_{timestamp}.xlsx"

#         df.to_excel(excel_file, index=False)
        
#         if files_count > 0:
#             analytics = UploadAnalytics(
#                 user_id=current_user.id,
#                 source="blinkit",
#                 pdf_count=files_count
#             )
#             db.add(analytics)
#             db.commit()

#         # Excel file schedule kar di download hone ke baad delete hone ke liye
#         background_tasks.add_task(remove_file, excel_file)

#         return FileResponse(
#             path=excel_file,
#             filename=excel_file,
#             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#     finally:
#         # Temporary PDFs ko safely clean up karna
#         for path in temp_paths:
#             remove_file(path)
            
            
            
# --------------------------------------------------------------------------------------------------------------------------------




# import os
# import re
# import tempfile
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor
# from typing import List

# import pdfplumber
# import pandas as pd
# from fastapi import Depends, UploadFile, File, BackgroundTasks
# from fastapi.responses import FileResponse
# from sqlalchemy.orm import Session

# from database.database import get_db
# from database.models import UploadAnalytics


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


# def remove_file(path: str):
#     """Callback function to safely delete files after response delivery"""
#     try:
#         if os.path.exists(path):
#             os.remove(path)
#     except Exception:
#         pass


# # ============================================
# # PROCESS PDF
# # ============================================

# def process_pdf(pdf_path):
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             if not pdf.pages:
#                 return {"File Name": os.path.basename(pdf_path), "Error": "PDF is empty"}
#             text = pdf.pages[0].extract_text() or ""

#         lines = [
#             line.strip()
#             for line in text.split("\n")
#             if line.strip()
#         ]

#         invoice_no = extract(r"Invoice No[:\s]+([A-Z0-9\-]+)", text)
#         invoice_date = extract(r"Invoice Date[:\s]+([0-9\-]+)", text)
#         merchant_name = extract(r"Entity Name[:\s]+(.*?)\s+State", text)
#         hsn_code = extract(r"HSN Code[:\s]+(\d+)", text)
#         service_desc = extract(r"Service Description[:\s]+(.*?)\s+Work Description", text)

#         period_start = ""
#         period_end = ""

#         period_match = re.search(
#             r"Period:\s*(.*?)\s+(?:To|to)\s+(.*)",
#             text
#         )

#         if period_match and len(period_match.groups()) >= 2:
#             period_start = period_match.group(1).strip()
#             period_end = period_match.group(2).strip()

#         gstin_matches = re.findall(
#             r"GSTIN[:\s]+([0-9A-Z]{15})",
#             text
#         )

#         company_gstin = gstin_matches[0] if len(gstin_matches) > 0 else ""
#         merchant_gstin = gstin_matches[1] if len(gstin_matches) > 1 else ""

#         particular = ""
#         particular_amount = 0.0

#         for line in lines:
#             match = re.match(
#                 r"^\d+\s+(.*?)\s+([\d,]+\.\d+)$",
#                 line
#             )
#             if match:
#                 particular = match.group(1).strip()
#                 particular_amount = to_float(match.group(2))
#                 break

#         taxable_amount = to_float(extract(r"Taxable Amount\s+([\d,]+\.\d+)", text))
        
#         sgst_rate = to_float(extract(r"SGST\s*@\s*([0-9.]+)", text))
#         sgst_amount = to_float(extract(r"SGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

#         cgst_rate = to_float(extract(r"CGST\s*@\s*([0-9.]+)", text))
#         cgst_amount = to_float(extract(r"CGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

#         igst_rate = to_float(extract(r"IGST\s*@\s*([0-9.]+)", text))
#         igst_amount = to_float(extract(r"IGST\s*@\s*[0-9.]+%?\s+([\d,]+\.\d+)", text))

#         total_amount = to_float(extract(r"Total Amount\s+([\d,]+\.\d+)", text))

#         return {
#             "File Name": os.path.basename(pdf_path),
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
#         }

#     except Exception as e:
#         return {
#             "File Name": os.path.basename(pdf_path),
#             "Error": str(e)
#         }


# # ============================================
# # API FUNCTION CALLED BY app.py
# # ============================================

# async def upload_blinkit(
#     background_tasks: BackgroundTasks,
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db),
#     current_user = None  # Removed strict User model annotation & Depends() requirement
# ):
#     files_count = len(files)
#     temp_paths = []

#     try:
#         for file in files:
#             tmp = tempfile.NamedTemporaryFile(
#                 delete=False,
#                 suffix=".pdf"
#             )
#             content = await file.read()
#             tmp.write(content)
#             tmp.close()
#             temp_paths.append(tmp.name)

#         with ThreadPoolExecutor(max_workers=8) as executor:
#             data = list(
#                 executor.map(
#                     process_pdf,
#                     temp_paths
#                 )
#             )

#         df = pd.DataFrame(data)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         excel_file = f"blinkit_invoice_details_{timestamp}.xlsx"

#         df.to_excel(excel_file, index=False)
        
#         # Log to database safely if user context exists
#         if files_count > 0 and current_user and hasattr(current_user, 'id'):
#             analytics = UploadAnalytics(
#                 user_id=current_user.id,
#                 source="blinkit",
#                 pdf_count=files_count
#             )
#             db.add(analytics)
#             db.commit()

#         # Schedule excel file cleanup after download
#         background_tasks.add_task(remove_file, excel_file)

#         return FileResponse(
#             path=excel_file,
#             filename=excel_file,
#             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#     finally:
#         # Safely clean up temporary PDFs
#         for path in temp_paths:
#             remove_file(path)







#jdh bdchj bdc njchd udhcdcdwjcbachuvccvchcbvh




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

async def upload_blinkit(
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
        excel_file = f"blinkit_invoice_details_{timestamp}.xlsx"

        df.to_excel(excel_file, index=False)
        
        # Log to database safely if user context exists
        if files_count > 0 and current_user and hasattr(current_user, 'id'):
            analytics = UploadAnalytics(
                user_id=current_user.id,
                source="blinkit",
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