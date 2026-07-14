# # backend/database/database.py

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base

# import os
# from dotenv import load_dotenv

# # Locate the .env file in the backend directory
# backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# dotenv_path = os.path.join(backend_dir, ".env")
# load_dotenv(dotenv_path=dotenv_path)

# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"sslmode": "require"},
#     pool_pre_ping=True,
#     pool_recycle=300
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# Base = declarative_base()


# def get_db():

#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()

# backend/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os
import urllib.parse
from dotenv import load_dotenv

# Locate the .env file in the backend directory
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(backend_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# --- URL ENCODING FIX FOR SPECIAL CHARACTERS IN PASSWORD ---
if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    try:
        # Split the URL scheme (postgresql://) from the rest of the string
        scheme, rest = DATABASE_URL.split("://", 1)
        
        # Split the credentials section from the host/database section
        if "@" in rest:
            credentials, host_db = rest.rsplit("@", 1)
            
            # Separate the username and password
            if ":" in credentials:
                username, password = credentials.split(":", 1)
                
                # URL-encode the password safely (turns '@' into '%40', etc.)
                encoded_password = urllib.parse.quote_plus(password)
                
                # Reconstruct the corrected DATABASE_URL
                DATABASE_URL = f"{scheme}://{username}:{encoded_password}@{host_db}"
    except Exception as e:
        # Fallback to the original URL if parsing fails for any reason
        print(f"Warning: Could not automatically encode database password: {e}")


engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()