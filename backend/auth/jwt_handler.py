from jose import jwt
from jose import JWTError
from jose import ExpiredSignatureError

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from dotenv import load_dotenv

import os


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")


if not SECRET_KEY:
    raise Exception(
        "SECRET_KEY missing"
    )


ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)


ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        1440
    )
)



def create_access_token(data: dict):


    payload = data.copy()


    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )


    payload.update({

        "exp": expire,

        "type": "access"

    })


    token = jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM

    )


    return token





def verify_token(token:str):


    try:


        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[
                ALGORITHM
            ]

        )


        if payload.get(
            "type"
        ) != "access":

            return None



        if not payload.get(
            "user_id"
        ):

            return None



        return payload



    except ExpiredSignatureError:

        return None



    except JWTError:

        return None