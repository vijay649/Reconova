# import requests
# import os

# BREVO_API_KEY = os.getenv("BREVO_API_KEY")


# def send_otp_email(
#     email: str,
#     otp: str
# ):

#     url = "https://api.brevo.com/v3/smtp/email"

#     payload = {

#         "sender": {
#             "name": "Reconova",
#             "email": "noreply@reconova.com"
#         },

#         "to": [
#             {
#                 "email": email
#             }
#         ],

#         "subject": "Email Verification OTP",

#         "htmlContent": f"""

#         <h2>Reconova Verification</h2>

#         <p>Your OTP is:</p>

#         <h1>{otp}</h1>

#         <p>Valid for 10 minutes.</p>

#         """
#     }

#     headers = {

#         "accept": "application/json",

#         "api-key": BREVO_API_KEY,

#         "content-type": "application/json"
#     }

#     requests.post(
#         url,
#         json=payload,
#         headers=headers
#     )


import os
import requests

from dotenv import load_dotenv

load_dotenv()
# print("EMAIL SERVICE LOADED")
# print("BREVO KEY =", BREVO_API_KEY)


def send_otp_email(
    email: str,
    otp: str
):

    BREVO_API_KEY = os.getenv(
        "BREVO_API_KEY"
    )

    print(
        "BREVO KEY FOUND:",
        bool(BREVO_API_KEY)
    )

    if not BREVO_API_KEY:

        print(
            "BREVO_API_KEY not found in .env"
        )

        return False

    url = (
        "https://api.brevo.com"
        "/v3/smtp/email"
    )

    payload = {

        "sender": {

            "name": "Reconova",

            "email":
            "vijaysharmagzb9625@gmail.com"
        },

        "to": [
            {
                "email": email
            }
        ],

        "subject":
        "Email Verification OTP",

        "htmlContent": f"""
        <h2>Reconova Verification</h2>

        <p>Your OTP is:</p>

        <h1>{otp}</h1>

        <p>Valid for 10 minutes.</p>
        """
    }

    headers = {

        "accept":
        "application/json",

        "api-key":
        BREVO_API_KEY,

        "content-type":
        "application/json"
    }

    try:

        response = requests.post(

            url,

            json=payload,

            headers=headers,

            timeout=30
        )

        print(
            "Brevo Status:",
            response.status_code
        )

        print(
            "Brevo Response:",
            response.text
        )

        if response.status_code in [
            200,
            201,
            202
        ]:

            print(
                f"OTP sent successfully to {email}"
            )

            return True

        print(
            "Brevo rejected request"
        )

        return False

    except requests.exceptions.RequestException as e:

        print(
            "Brevo Connection Error:",
            str(e)
        )

        return False

    except Exception as e:

        print(
            "Unexpected Email Error:",
            str(e)
        )

        return False