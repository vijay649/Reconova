
STEP 1
Install Python

STEP 2
Open CMD in backend folder

STEP 3
Install packages:

pip install -r requirements.txt

STEP 4
Run backend:

uvicorn app:app --reload

STEP 5
Open frontend/index.html

STEP 6
Upload PDFs and click Generate Excel

IMPORTANT:
Backend CMD window must stay running.





CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    fullname VARCHAR(100),
    email VARCHAR(200) UNIQUE,
    password VARCHAR(255)
);