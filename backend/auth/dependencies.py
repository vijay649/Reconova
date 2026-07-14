# # from fastapi import Depends
# # from fastapi import HTTPException
# # from fastapi.security import HTTPBearer
# # from fastapi.security import HTTPAuthorizationCredentials

# # from auth.jwt_handler import verify_token
# # from sqlalchemy.orm import Session

# # from database.database import get_db
# # from database.models import User


# # security = HTTPBearer()


# # def get_current_user(

# #     credentials: HTTPAuthorizationCredentials = Depends(security),

# #     db: Session = Depends(get_db)

# # ):

# #     token = credentials.credentials

# #     payload = verify_token(token)

# #     if not payload:

# #         raise HTTPException(
# #             status_code=401,
# #             detail="Invalid token"
# #         )
        

# #     user = db.query(User).filter(
# #         User.id == payload["user_id"]
# #     ).first()

# #     if not user:

# #         raise HTTPException(
# #             status_code=404,
# #             detail="User not found"
# #         )

# #     return user

# #     # return payload


# from fastapi import Depends
# from fastapi import HTTPException
# from fastapi import status

# from fastapi.security import HTTPBearer
# from fastapi.security import HTTPAuthorizationCredentials


# from sqlalchemy.orm import Session


# from auth.jwt_handler import verify_token

# from database.database import get_db

# from database.models import User



# security = HTTPBearer()





# def get_current_user(

#     credentials: HTTPAuthorizationCredentials = Depends(
#         security
#     ),

#     db: Session = Depends(get_db)

# ):


#     # =====================================
#     # GET TOKEN
#     # =====================================

#     if not credentials:


#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Authentication token required"

#         )



#     token = credentials.credentials



#     # =====================================
#     # VERIFY TOKEN
#     # =====================================

#     payload = verify_token(token)



#     if not payload:


#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Invalid or expired token"

#         )



#     # =====================================
#     # CHECK USER ID IN TOKEN
#     # =====================================

#     user_id = payload.get(
#         "user_id"
#     )



#     if not user_id:


#         raise HTTPException(

#             status_code=status.HTTP_401_UNAUTHORIZED,

#             detail="Invalid token payload"

#         )



#     # =====================================
#     # FETCH USER
#     # =====================================

#     user = db.query(User).filter(

#         User.id == user_id

#     ).first()



#     if not user:


#         raise HTTPException(

#             status_code=status.HTTP_404_NOT_FOUND,

#             detail="User not found"

#         )



#     # =====================================
#     # ACTIVE USER CHECK
#     # =====================================

#     if hasattr(user, "is_active"):


#         if not user.is_active:


#             raise HTTPException(

#                 status_code=status.HTTP_403_FORBIDDEN,

#                 detail="Account disabled"

#             )



#     return user


# backend/auth/dependencies.py


from fastapi import Depends
from fastapi import HTTPException
from fastapi import status


from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials


from sqlalchemy.orm import Session


from auth.jwt_handler import verify_token

from database.database import get_db

from database.models import User





# ==========================================
# JWT SECURITY
# ==========================================

security = HTTPBearer(
    auto_error=False
)






# ==========================================
# GET CURRENT LOGGED IN USER
# ==========================================

def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),

    db: Session = Depends(get_db)

):


    # ======================================
    # TOKEN CHECK
    # ======================================

    if not credentials:


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Authentication token required"

        )



    token = credentials.credentials




    # ======================================
    # VERIFY JWT TOKEN
    # ======================================

    payload = verify_token(
        token
    )



    if not payload:


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid or expired token"

        )





    # ======================================
    # GET USER ID FROM TOKEN
    # ======================================

    user_id = payload.get(
        "user_id"
    )



    if not user_id:


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token data"

        )





    # ======================================
    # FETCH USER FROM DATABASE
    # ======================================

    user = db.query(User).filter(

        User.id == user_id

    ).first()




    if not user:


        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="User not found"

        )





    # ======================================
    # ACCOUNT STATUS CHECK
    # ======================================

    if hasattr(user, "is_active"):


        if user.is_active is False:


            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Your account has been disabled"

            )





    return user