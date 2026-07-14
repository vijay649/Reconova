# backend/database/models.py


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from .database import Base

# from .database.database import Base

# =====================================================
# USER TABLE
# =====================================================

class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String(100),
        nullable=False
    )


    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )


    password_hash = Column(
        String(255),
        nullable=False
    )


    role = Column(
        String(20),
        default="user"
    )


    is_verified = Column(
        Boolean,
        default=False
    )


    # Account status
    is_active = Column(
        Boolean,
        default=True
    )


    # Login tracking
    last_login = Column(
        DateTime,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



    # ================================
    # RELATIONSHIPS
    # ================================


    uploads = relationship(

        "UploadAnalytics",

        back_populates="user",

        cascade="all, delete",

        passive_deletes=True

    )



    upload_history = relationship(

        "UploadHistory",

        back_populates="user",

        cascade="all, delete",

        passive_deletes=True

    )



    otp_codes = relationship(

        "OTPCode",

        back_populates="user",

        cascade="all, delete",

        passive_deletes=True

    )



# =====================================================
# OTP TABLE
# =====================================================


class OTPCode(Base):

    __tablename__ = "otp_codes"



    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    user_id = Column(

        Integer,

        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )

    )


    otp = Column(

        String(6),

        nullable=False

    )


    expires_at = Column(

        DateTime

    )



    user = relationship(

        "User",

        back_populates="otp_codes"

    )



# =====================================================
# UPLOAD HISTORY TABLE
# =====================================================


class UploadHistory(Base):

    __tablename__ = "upload_history"



    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    user_id = Column(

        Integer,

        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )

    )


    source = Column(

        String(50)

    )


    pdf_count = Column(

        Integer,

        default=0

    )


    uploaded_at = Column(

        DateTime,

        default=datetime.utcnow

    )



    user = relationship(

        "User",

        back_populates="upload_history"

    )




# =====================================================
# UPLOAD ANALYTICS TABLE
# =====================================================


class UploadAnalytics(Base):

    __tablename__ = "upload_analytics"



    id = Column(

        Integer,

        primary_key=True,

        index=True

    )



    user_id = Column(

        Integer,

        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )

    )



    source = Column(

        String(50),

        nullable=False

    )



    pdf_count = Column(

        Integer,

        default=0

    )



    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )



    user = relationship(

        "User",

        back_populates="uploads"

    )





# =====================================================
# ADMIN ACTIVITY LOG
# =====================================================


class AdminActivityLog(Base):

    __tablename__ = "admin_activity_logs"



    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    admin_id = Column(

        Integer,

        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )

    )


    action = Column(

        String(255),

        nullable=False

    )


    target_user_id = Column(

        Integer,

        nullable=True

    )


    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


    admin = relationship(

        "User"

    )