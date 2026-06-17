# backend/app.py


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



# =====================================
# DATABASE
# =====================================

from database.database import engine
from database.models import Base



# Create Tables

Base.metadata.create_all(
    bind=engine
)




# =====================================
# PARSER IMPORTS
# =====================================

from parsers.amazon import upload_amazon
from parsers.swiggy import upload_swiggy
from parsers.zomato import upload_zomato
from parsers.blinkit import upload_blinkit
from parsers.flipkart import upload_flipkart




# =====================================
# ROUTERS
# =====================================

from routers.auth_router import router as auth_router

from routers.admin_router import router as admin_router

from routers.dashboard_router import router as dashboard_router





# =====================================
# FASTAPI APP
# =====================================


app = FastAPI(

    title="Reconova API",

    version="1.0"

)





# =====================================
# CORS
# =====================================


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)






# =====================================
# INCLUDE ROUTERS
# =====================================


app.include_router(
    auth_router
)


app.include_router(
    admin_router
)


app.include_router(
    dashboard_router
)






# =====================================
# HOME
# =====================================


@app.get("/")

def home():

    return {

        "message":
        "Reconova Backend Running"

    }






# =====================================
# PARSER APIs
# =====================================


app.post("/amazon")(
    upload_amazon
)


app.post("/swiggy")(
    upload_swiggy
)


app.post("/zomato")(
    upload_zomato
)


app.post("/blinkit")(
    upload_blinkit
)


app.post("/flipkart")(
    upload_flipkart
)