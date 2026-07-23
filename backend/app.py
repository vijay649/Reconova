# # ----------------------------------------------------------------------------------------------------------

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from backend.database.database import engine
# # from database.database import engine
# from database.models import Base
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from database.database import get_db
# from database.models import User, UploadAnalytics # Base analytics tracking models if used

# Base.metadata.create_all(bind=engine)

# from routers.auth_router import router as auth_router
# from routers.dashboard_router import router as dashboard_router
# from routers.admin_router import router as admin_router
# from parsers.amazon import upload_amazon
# from parsers.swiggy import upload_swiggy
# from parsers.zomato import upload_zomato
# from parsers.blinkit import upload_blinkit
# from parsers.flipkart import upload_flipkart

# app = FastAPI(
#     title="Reconova API",
#     description="Invoice Reconciliation SaaS Backend",
#     version="1.0.0"
# )

# # =====================================================
# # CORS (FIXED WITH EXPOSE HEADERS FOR DOWNLOADS)
# # =====================================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Content-Disposition"],
# )

# # =====================================================
# # INCLUDE ROUTERS
# # =====================================================
# app.include_router(auth_router)
# app.include_router(dashboard_router)
# app.include_router(admin_router)

# # =====================================================
# # FIXED MISSING STATS ENDPOINTS (To solve 404 errors)
# # =====================================================
# @app.get("/admin/total-users")
# def get_total_users(db: Session = Depends(get_db)):
#     try:
#         count = db.query(User).count()
#         return {"total_users": count}
#     except:
#         return {"total_users": 0}

# @app.get("/admin/verified-users")
# def get_verified_users(db: Session = Depends(get_db)):
#     try:
#         # Assuming you have a verified column or tracking
#         count = db.query(User).filter(User.verified == True).count()
#         return {"verified_users": count}
#     except:
#         return {"verified_users": 0}

# @app.get("/admin/total-uploads")
# def get_total_uploads(db: Session = Depends(get_db)):
#     try:
#         count = db.query(UploadAnalytics).count()
#         return {"total_uploads": count}
#     except:
#         return {"total_uploads": 0}


# # =====================================================
# # PARSER ROUTES
# # =====================================================
# app.post("/amazon")(upload_amazon)
# app.post("/swiggy")(upload_swiggy)
# app.post("/zomato")(upload_zomato)
# app.post("/blinkit")(upload_blinkit)
# app.post("/flipkart")(upload_flipkart)

# # =====================================================
# # HOME & HEALTH
# # =====================================================
# @app.get("/")
# def home():
#     return {"message": "Reconova Backend Running", "status": "active"}

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.on_event("startup")
# def startup_event():
#     print("🚀 Reconova API Started Successfully")





# # ----------------------------------------------------------------------------------------------------------

# from fastapi import FastAPI, BackgroundTasks, Depends, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session

# # Safe imports for engine and tables
# try:
#     from backend.database.database import engine, get_db
# except ModuleNotFoundError:
#     from database.database import engine, get_db

# from database.models import Base, User, UploadAnalytics

# Base.metadata.create_all(bind=engine)

# from routers.auth_router import router as auth_router
# from routers.dashboard_router import router as dashboard_router
# from routers.admin_router import router as admin_router

# # Parsers Imports
# from parsers.amazon import upload_amazon
# from parsers.swiggy import upload_swiggy
# from parsers.zomato import upload_zomato
# from parsers.blinkit import upload_blinkit
# from parsers.flipkart import upload_flipkart

# app = FastAPI(
#     title="Reconova API",
#     description="Invoice Reconciliation SaaS Backend",
#     version="1.0.0"
# )

# # =====================================================
# # CORS (FIXED WITH EXPOSE HEADERS FOR DOWNLOADS)
# # =====================================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Content-Disposition"],
# )

# # =====================================================
# # INCLUDE ROUTERS
# # =====================================================
# app.include_router(auth_router)
# app.include_router(dashboard_router)
# app.include_router(admin_router)

# # =====================================================
# # FIXED MISSING STATS ENDPOINTS
# # =====================================================
# @app.get("/admin/total-users")
# def get_total_users(db: Session = Depends(get_db)):
#     try:
#         count = db.query(User).count()
#         return {"total_users": count}
#     except:
#         return {"total_users": 0}

# @app.get("/admin/verified-users")
# def get_verified_users(db: Session = Depends(get_db)):
#     try:
#         count = db.query(User).filter(User.verified == True).count()
#         return {"verified_users": count}
#     except:
#         return {"verified_users": 0}

# @app.get("/admin/total-uploads")
# def get_total_uploads(db: Session = Depends(get_db)):
#     try:
#         count = db.query(UploadAnalytics).count()
#         return {"total_uploads": count}
#     except:
#         return {"total_uploads": 0}


# # =====================================================
# # PARSER ROUTES (FIXED FOR BACKGROUND TASKS)
# # =====================================================
# app.post("/amazon")(upload_amazon)
# app.post("/swiggy")(upload_swiggy)
# app.post("/zomato")(upload_zomato)
# app.post("/flipkart")(upload_flipkart)

# # Blinkit route explicitly handled for background tasks injection
# @app.post("/blinkit")
# async def blinkit_endpoint(
#     background_tasks: BackgroundTasks,
#     files: list[UploadFile] = File(...),
#     db: Session = Depends(get_db)
# ):
#     # Calling the upload_blinkit directly and passing background_tasks
#     return await upload_blinkit(background_tasks=background_tasks, files=files, db=db)


# # =====================================================
# # HOME & HEALTH
# # =====================================================
# @app.get("/")
# def home():
#     return {"message": "Reconova Backend Running", "status": "active"}

# @app.get("/health")
# def health():
#     return {"status": "ok"}

# @app.on_event("startup")
# def startup_event():
#     print("🚀 Reconova API Started Successfully")

#--------------------------------------------------------------------------------------------------------------------------







# import sys
# import os

# # Ensure the backend directory is in python's search path
# backend_dir = os.path.dirname(os.path.abspath(__file__))
# if backend_dir not in sys.path:
#     sys.path.insert(0, backend_dir)

# from fastapi import FastAPI, BackgroundTasks, Depends, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from typing import List
# import uvicorn

# try:
#     from backend.database.database import engine, get_db
# except ModuleNotFoundError:
#     from database.database import engine, get_db

# from database.models import Base, User, UploadAnalytics

# Base.metadata.create_all(bind=engine)

# from routers.auth_router import router as auth_router
# from routers.dashboard_router import router as dashboard_router
# from routers.admin_router import router as admin_router
# from auth.dependencies import get_current_user

# from parsers.amazon import upload_amazon
# from parsers.swiggy import upload_swiggy
# from parsers.zomato import upload_zomato
# from parsers.blinkit import upload_blinkit
# from parsers.flipkart import upload_flipkart

# app = FastAPI(
#     title="Reconova API",
#     description="Invoice Reconciliation SaaS Backend",
#     version="1.0.0"
# )

# origins = [
#     "http://localhost:5173", # Vite ka local port
#     "http://127.0.0.1:5173",
# ]

# # =====================================================
# # CORS FIXED FOR ALL INCOMING ROUTE STATUSES (502 / 500 INCLUDED)
# # =====================================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Render free tier ke liye wildcard sabse safe hai taaki error status block na ho
#     allow_credentials=False, 
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Content-Disposition", "Content-Type"],
# )

# app.include_router(auth_router)
# app.include_router(dashboard_router)
# app.include_router(admin_router)

# @app.get("/admin/total-users")
# def get_total_users(db: Session = Depends(get_db)):
#     try:
#         return {"total_users": db.query(User).count()}
#     except:
#         return {"total_users": 0}

# @app.get("/admin/verified-users")
# def get_verified_users(db: Session = Depends(get_db)):
#     try:
#         return {"verified_users": db.query(User).filter(User.verified == True).count()}
#     except:
#         return {"verified_users": 0}

# @app.get("/admin/total-uploads")
# def get_total_uploads(db: Session = Depends(get_db)):
#     try:
#         return {"total_uploads": db.query(UploadAnalytics).count()}
#     except:
#         return {"total_uploads": 0}

# # =====================================================
# # PARSER ENDPOINTS (WITH MEMORY & FAULT SAFETY)
# # =====================================================
# app.post("/amazon")(upload_amazon)
# app.post("/swiggy")(upload_swiggy)
# app.post("/flipkart")(upload_flipkart)

# @app.post("/zomato")
# async def zomato_endpoint(
#     background_tasks: BackgroundTasks,
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files uploaded")
#     try:
#         return await upload_zomato(
#             background_tasks=background_tasks,
#             files=files,
#             db=db,
#             current_user=current_user
#         )
#     except Exception as e:
#         print(f"Zomato Parser Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Parser execution failed: {str(e)}")

# @app.post("/blinkit")
# async def blinkit_endpoint(
#     background_tasks: BackgroundTasks,
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db)
# ):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files uploaded")
#     try:
#         return await upload_blinkit(background_tasks=background_tasks, files=files, db=db)
#     except Exception as e:
#         print(f"Blinkit Parser Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/")
# def home():
#     return {"message": "Reconova Backend Running", "status": "active"}

# @app.get("/health")
# def health():
#     return {"status": "ok"}



# ----------------------------------------------------------------------------------------------------------------------



# import sys
# import os

# # Ensure the backend directory is in python's search path
# backend_dir = os.path.dirname(os.path.abspath(__file__))
# if backend_dir not in sys.path:
#     sys.path.insert(0, backend_dir)

# from fastapi import FastAPI, BackgroundTasks, Depends, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from typing import List, Optional
# import uvicorn

# try:
#     from backend.database.database import engine, get_db
# except ModuleNotFoundError:
#     from database.database import engine, get_db

# from database.models import Base, User, UploadAnalytics

# Base.metadata.create_all(bind=engine)

# from routers.auth_router import router as auth_router
# from routers.dashboard_router import router as dashboard_router
# from routers.admin_router import router as admin_router

# from parsers.amazon import upload_amazon
# from parsers.swiggy import upload_swiggy
# from parsers.zomato import upload_zomato
# from parsers.blinkit import upload_blinkit
# from parsers.flipkart import upload_flipkart

# app = FastAPI(
#     title="Reconova API",
#     description="Invoice Reconciliation SaaS Backend",
#     version="1.0.0"
# )

# # =====================================================
# # CORS FIXED FOR ALL INCOMING ROUTE STATUSES
# # =====================================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=False, 
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Content-Disposition", "Content-Type"],
# )

# app.include_router(auth_router)
# app.include_router(dashboard_router)
# app.include_router(admin_router)

# @app.get("/admin/total-users")
# def get_total_users(db: Session = Depends(get_db)):
#     try:
#         return {"total_users": db.query(User).count()}
#     except:
#         return {"total_users": 0}

# @app.get("/admin/verified-users")
# def get_verified_users(db: Session = Depends(get_db)):
#     try:
#         return {"verified_users": db.query(User).filter(User.verified == True).count()}
#     except:
#         return {"verified_users": 0}

# @app.get("/admin/total-uploads")
# def get_total_uploads(db: Session = Depends(get_db)):
#     try:
#         return {"total_uploads": db.query(UploadAnalytics).count()}
#     except:
#         return {"total_uploads": 0}

# # =====================================================
# # PARSER ENDPOINTS (UNIFORM & FAULT SAFE)
# # =====================================================
# app.post("/amazon")(upload_amazon)
# app.post("/swiggy")(upload_swiggy)
# app.post("/flipkart")(upload_flipkart)

# @app.post("/zomato")
# async def zomato_endpoint(
#     background_tasks: BackgroundTasks,
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db),
#     # Made current_user optional so public/guest uploads won't fail with 401 Unauthorized
#     current_user: Optional[dict] = None
# ):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files uploaded")
#     try:
#         return await upload_zomato(
#             background_tasks=background_tasks,
#             files=files,
#             db=db,
#             current_user=current_user
#         )
#     except Exception as e:
#         print(f"Zomato Parser Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Parser execution failed: {str(e)}")

# @app.post("/blinkit")
# async def blinkit_endpoint(
#     background_tasks: BackgroundTasks,
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db)
# ):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files uploaded")
#     try:
#         return await upload_blinkit(background_tasks=background_tasks, files=files, db=db)
#     except Exception as e:
#         print(f"Blinkit Parser Error: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/")
# def home():
#     return {"message": "Reconova Backend Running", "status": "active"}

# @app.get("/health")
# def health():
#     return {"status": "ok"}




# --------------------------------------------------------------------------------------------------------------------------------



import os
import sys

# Ensure the backend directory is in python's search path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import uvicorn
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Database imports with fallback safety
try:
    from backend.database.database import engine, get_db
    from backend.database.models import Base, User, UploadAnalytics
except ModuleNotFoundError:
    from database.database import engine, get_db
    from database.models import Base, User, UploadAnalytics

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Routers
from routers.auth_router import router as auth_router
from routers.dashboard_router import router as dashboard_router
from routers.admin_router import router as admin_router

# Parser Handlers
from parsers.amazon import upload_amazon
from parsers.swiggy import upload_swiggy
from parsers.zomato import upload_zomato
from parsers.blinkit import upload_blinkit
from parsers.flipkart import upload_flipkart

app = FastAPI(
    title="Reconova API",
    description="Invoice Reconciliation SaaS Backend",
    version="1.0.0"
)

# =====================================================
# CORS CONFIGURATION (FIXED FOR VERCEL + AXIOS)
# =====================================================
origins = [
    "https://amzn-inv.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Set to True so headers/tokens pass through cleanly
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "Content-Disposition", 
        "Content-Type", 
        "Access-Control-Expose-Headers"
    ],
)

# Register Router Blueprints
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(admin_router)


# =====================================================
# ADMIN METRICS ENDPOINTS
# =====================================================
@app.get("/admin/total-users")
def get_total_users(db: Session = Depends(get_db)):
    try:
        return {"total_users": db.query(User).count()}
    except Exception:
        return {"total_users": 0}

@app.get("/admin/verified-users")
def get_verified_users(db: Session = Depends(get_db)):
    try:
        return {"verified_users": db.query(User).filter(User.verified == True).count()}
    except Exception:
        return {"verified_users": 0}

@app.get("/admin/total-uploads")
def get_total_uploads(db: Session = Depends(get_db)):
    try:
        return {"total_uploads": db.query(UploadAnalytics).count()}
    except Exception:
        return {"total_uploads": 0}


# =====================================================
# PARSER ENDPOINTS (REGISTERED DIRECTLY TO RETAIN CORS)
# =====================================================
app.post("/amazon")(upload_amazon)
app.post("/flipkart")(upload_flipkart)
app.post("/swiggy")(upload_swiggy)
app.post("/zomato")(upload_zomato)
app.post("/blinkit")(upload_blinkit)


# =====================================================
# HEALTH & BASE ENDPOINTS
# =====================================================
@app.get("/")
def home():
    return {"message": "Reconova Backend Running", "status": "active"}

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)