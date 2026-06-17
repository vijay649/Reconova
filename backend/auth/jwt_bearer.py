# @router.get("/me")
# def get_current_user(
#     current_user=Depends(JWTBearer())
# ):
#     return current_user

from fastapi import Request
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from jose import jwt

from auth.jwt_handler import SECRET_KEY
from auth.jwt_handler import ALGORITHM


class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = (
            await super().__call__(request)
        )

        if not credentials:

            raise HTTPException(
                status_code=403,
                detail="Invalid token"
            )

        try:

            payload = jwt.decode(
                credentials.credentials,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            return payload

        except:

            raise HTTPException(
                status_code=403,
                detail="Token expired"
            )