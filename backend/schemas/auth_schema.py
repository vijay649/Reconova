# backend/schemas/auth_schema.py


from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field





# =====================================================
# SIGNUP
# =====================================================


class SignupSchema(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=100
    )


    email: EmailStr


    password: str = Field(

        min_length=6

    )







# =====================================================
# LOGIN
# =====================================================


class LoginSchema(BaseModel):

    email: EmailStr


    password: str







# =====================================================
# VERIFY OTP
# =====================================================


class VerifyOTPSchema(BaseModel):


    email: EmailStr


    otp: str = Field(

        min_length=4,

        max_length=6

    )







# =====================================================
# FORGOT PASSWORD
# =====================================================


class ForgotPasswordSchema(BaseModel):


    email: EmailStr







# =====================================================
# RESET PASSWORD
# =====================================================


class ResetPasswordSchema(BaseModel):


    email: EmailStr


    otp: str = Field(

        min_length=4,

        max_length=6

    )


    new_password: str = Field(

        min_length=6

    )