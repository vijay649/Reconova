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
from fastapi import FastAPI, BackgroundTasks, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Safe imports for engine and tables
try:
    from backend.database.database import engine, get_db
except ModuleNotFoundError:
    from database.database import engine, get_db

from database.models import Base, User, UploadAnalytics

Base.metadata.create_all(bind=engine)

from routers.auth_router import router as auth_router
from routers.dashboard_router import router as dashboard_router
from routers.admin_router import router as admin_router

# Auth Dependency Import for endpoint injection
from auth.dependencies import get_current_user

# Parsers Imports
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
# CORS (FIXED WITH EXPLICIT ORIGINS & EXPOSED HEADERS FOR BULK DOWNLOADS)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://amzn-inv.vercel.app",  # Aapki active frontend deployment URL
        "http://localhost:3000",        # Local testing ke liye
        "http://127.0.0.1:5500",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Type"],
)

# =====================================================
# INCLUDE ROUTERS
# =====================================================
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(admin_router)

# =====================================================
# FIXED MISSING STATS ENDPOINTS
# =====================================================
@app.get("/admin/total-users")
def get_total_users(db: Session = Depends(get_db)):
    try:
        count = db.query(User).count()
        return {"total_users": count}
    except:
        return {"total_users": 0}

@app.get("/admin/verified-users")
def get_verified_users(db: Session = Depends(get_db)):
    try:
        count = db.query(User).filter(User.verified == True).count()
        return {"verified_users": count}
    except:
        return {"verified_users": 0}

@app.get("/admin/total-uploads")
def get_total_uploads(db: Session = Depends(get_db)):
    try:
        count = db.query(UploadAnalytics).count()
        return {"total_uploads": count}
    except:
        return {"total_uploads": 0}


# =====================================================
# PARSER ROUTES (FIXED FOR BACKGROUND TASKS & CURRENT USER)
# =====================================================
app.post("/amazon")(upload_amazon)
app.post("/swiggy")(upload_swiggy)
app.post("/flipkart")(upload_flipkart)

# Zomato route with background tasks injection and current_user dependency
@app.post("/zomato")
async def zomato_endpoint(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await upload_zomato(
        background_tasks=background_tasks,
        files=files,
        db=db,
        current_user=current_user
    )

# Blinkit route explicitly handled for background tasks injection
@app.post("/blinkit")
async def blinkit_endpoint(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    return await upload_blinkit(background_tasks=background_tasks, files=files, db=db)


# =====================================================
# HOME & HEALTH
# =====================================================
@app.get("/")
def home():
    return {"message": "Reconova Backend Running", "status": "active"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.on_event("startup")
def startup_event():
    print("🚀 Reconova API Started Successfully")