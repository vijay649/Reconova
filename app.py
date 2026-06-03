# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from parsers.amazon import upload_amazon
# from parsers.swiggy import upload_swiggy
# from parsers.zomato import upload_zomato

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def home():
#     return {
#         "message": "Reconova API Running"
#     }

# app.post("/amazon")(upload_amazon)

# app.post("/swiggy")(upload_swiggy)

# app.post("/zomato")(upload_zomato)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from parsers.amazon import upload_amazon
from parsers.swiggy import upload_swiggy
from parsers.zomato import upload_zomato

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Reconova Backend Running"
    }

app.post("/amazon")(upload_amazon)
app.post("/swiggy")(upload_swiggy)
app.post("/zomato")(upload_zomato)