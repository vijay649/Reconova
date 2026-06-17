# backend/routers/auth_router.py


from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException


from sqlalchemy.orm import Session


from datetime import datetime
from datetime import timedelta



from database.database import get_db


from database.models import (
    User,
    OTPCode
)



from schemas.auth_schema import (
    SignupSchema,
    LoginSchema,
    VerifyOTPSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema
)



from auth.password import (
    hash_password,
    verify_password
)



from auth.jwt_handler import (
    create_access_token
)



from auth.otp_service import generate_otp

from auth.email_service import send_otp_email





router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)





# =====================================================
# SIGNUP
# =====================================================


@router.post("/signup")
def signup(

    payload: SignupSchema,

    db: Session = Depends(get_db)

):


    user_exist = db.query(User).filter(

        User.email == payload.email

    ).first()



    if user_exist:

        raise HTTPException(

            status_code=400,

            detail="Email already exists"

        )




    user = User(

        name=payload.name,

        email=payload.email,

        password_hash=hash_password(
            payload.password
        ),

        role="user",

        is_active=True

    )



    db.add(user)

    db.commit()

    db.refresh(user)





    otp = generate_otp()



    otp_record = OTPCode(

        user_id=user.id,

        otp=otp,

        expires_at=

        datetime.utcnow()
        +
        timedelta(minutes=10)

    )



    db.add(otp_record)

    db.commit()




    send_otp_email(

        user.email,

        otp

    )



    return {

        "message":
        "OTP sent successfully"

    }







# =====================================================
# VERIFY OTP
# =====================================================


@router.post("/verify-otp")
def verify_otp(

    payload: VerifyOTPSchema,

    db: Session = Depends(get_db)

):


    user = db.query(User).filter(

        User.email == payload.email

    ).first()



    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )





    otp_record = db.query(OTPCode).filter(

        OTPCode.user_id == user.id,

        OTPCode.otp == payload.otp

    ).first()




    if not otp_record:

        raise HTTPException(

            status_code=400,

            detail="Invalid OTP"

        )





    if otp_record.expires_at < datetime.utcnow():


        db.delete(otp_record)

        db.commit()


        raise HTTPException(

            status_code=400,

            detail="OTP expired"

        )





    user.is_verified = True



    db.delete(otp_record)


    db.commit()




    return {


        "message":

        "Email verified successfully"


    }









# =====================================================
# LOGIN
# =====================================================


@router.post("/login")
def login(

    payload: LoginSchema,

    db: Session = Depends(get_db)

):


    user = db.query(User).filter(

        User.email == payload.email

    ).first()



    if not user:


        raise HTTPException(

            status_code=401,

            detail="Invalid email"

        )




    if not user.is_verified:


        raise HTTPException(

            status_code=401,

            detail="Email not verified"

        )




    if not user.is_active:


        raise HTTPException(

            status_code=403,

            detail="Account disabled"

        )





    if not verify_password(

        payload.password,

        user.password_hash

    ):


        raise HTTPException(

            status_code=401,

            detail="Invalid password"

        )




    user.last_login = datetime.utcnow()


    db.commit()





    token = create_access_token({

        "user_id":user.id,

        "email":user.email,

        "role":user.role

    })





    return {


        "access_token":token,


        "token_type":"bearer",



        "user":{


            "id":user.id,

            "name":user.name,

            "email":user.email,

            "role":user.role,
            
            "is_verified":user.is_verified,

            "is_active":user.is_active,
            
            "last_login":user.last_login
        }


    }









# =====================================================
# FORGOT PASSWORD
# =====================================================


@router.post("/forgot-password")
def forgot_password(

    payload: ForgotPasswordSchema,

    db: Session = Depends(get_db)

):


    user = db.query(User).filter(

        User.email == payload.email

    ).first()



    if not user:


        raise HTTPException(

            status_code=404,

            detail="User not found"

        )





    otp = generate_otp()



    otp_record = OTPCode(

        user_id=user.id,

        otp=otp,

        expires_at=

        datetime.utcnow()
        +
        timedelta(minutes=10)

    )



    db.add(otp_record)

    db.commit()



    send_otp_email(

        user.email,

        otp

    )



    return {


        "message":

        "Password reset OTP sent"


    }









# =====================================================
# RESET PASSWORD
# =====================================================


@router.post("/reset-password")
def reset_password(

    payload: ResetPasswordSchema,

    db: Session = Depends(get_db)

):


    user = db.query(User).filter(

        User.email == payload.email

    ).first()



    if not user:


        raise HTTPException(

            status_code=404,

            detail="User not found"

        )





    otp_record = db.query(OTPCode).filter(

        OTPCode.user_id == user.id,

        OTPCode.otp == payload.otp

    ).first()



    if not otp_record:


        raise HTTPException(

            status_code=400,

            detail="Invalid OTP"

        )





    user.password_hash = hash_password(

        payload.new_password

    )



    db.delete(otp_record)


    db.commit()




    return {


        "message":

        "Password reset successful"


    }