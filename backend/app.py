# ----------------------------------------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.database import engine
from database.models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User, UploadAnalytics # Base analytics tracking models if used

Base.metadata.create_all(bind=engine)

from routers.auth_router import router as auth_router
from routers.dashboard_router import router as dashboard_router
from routers.admin_router import router as admin_router
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
# CORS (FIXED WITH EXPOSE HEADERS FOR DOWNLOADS)
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# =====================================================
# INCLUDE ROUTERS
# =====================================================
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(admin_router)

# =====================================================
# FIXED MISSING STATS ENDPOINTS (To solve 404 errors)
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
        # Assuming you have a verified column or tracking
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
# PARSER ROUTES
# =====================================================
app.post("/amazon")(upload_amazon)
app.post("/swiggy")(upload_swiggy)
app.post("/zomato")(upload_zomato)
app.post("/blinkit")(upload_blinkit)
app.post("/flipkart")(upload_flipkart)

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