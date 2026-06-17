# backend/routers/admin_router.py


from auth.admin_required import admin_required


from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException


from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import desc


from database.database import get_db


from database.models import (
    User,
    UploadAnalytics,
    OTPCode
)



router = APIRouter(

    prefix="/admin",

    tags=["Admin"]

)





# =====================================================
# ADMIN DASHBOARD SUMMARY
# =====================================================


@router.get("/summary")
def admin_summary(

    db: Session = Depends(get_db),

    admin=Depends(admin_required)

):


    total_users = db.query(
        User
    ).count()



    verified_users = db.query(
        User
    ).filter(

        User.is_verified == True

    ).count()



    active_users = db.query(
        User
    ).filter(

        User.is_active == True

    ).count()




    total_uploads = db.query(

        func.sum(
            UploadAnalytics.pdf_count
        )

    ).scalar()



    return {


        "total_users":
        total_users,


        "verified_users":
        verified_users,


        "active_users":
        active_users,


        "total_uploads":
        total_uploads or 0

    }








# =====================================================
# ALL USERS LIST
# =====================================================


@router.get("/users")
def get_users(

    db: Session = Depends(get_db),

    admin=Depends(admin_required)

):


    users = db.query(
        User
    ).order_by(

        desc(
            User.created_at
        )

    ).all()



    result=[]



    for user in users:


        uploads = db.query(

            func.sum(
                UploadAnalytics.pdf_count
            )

        ).filter(

            UploadAnalytics.user_id ==
            user.id

        ).scalar()



        parsers = db.query(

            UploadAnalytics.source

        ).filter(

            UploadAnalytics.user_id ==
            user.id

        ).distinct().all()



        result.append({


            "id":
            user.id,


            "name":
            user.name,


            "email":
            user.email,


            "role":
            user.role,


            "verified":
            user.is_verified,


            "active":
            user.is_active,


            "total_uploads":
            uploads or 0,


            "parsers":

            [
                p[0]
                for p in parsers
            ],



            "last_login":
            user.last_login,


            "created_at":
            user.created_at

        })



    return result







# =====================================================
# PARSER ANALYTICS
# =====================================================


@router.get("/parser-analytics")
def parser_analytics(

    db: Session = Depends(get_db),

    admin=Depends(admin_required)

):


    data = db.query(

        UploadAnalytics.source,

        func.sum(
            UploadAnalytics.pdf_count
        )

    ).group_by(

        UploadAnalytics.source

    ).all()



    return [


        {

            "parser":
            row[0],


            "total_files":
            row[1] or 0

        }


        for row in data

    ]









# =====================================================
# USER ACTIVITY
# =====================================================


@router.get("/user-activity")
def user_activity(

    db:Session = Depends(get_db),

    admin=Depends(admin_required)

):


    records = db.query(

        UploadAnalytics

    ).order_by(

        desc(
            UploadAnalytics.created_at
        )

    ).all()



    result=[]



    for item in records:


        user = db.query(
            User
        ).filter(

            User.id ==
            item.user_id

        ).first()



        if user:


            result.append({


                "user_id":
                user.id,


                "user":
                user.name,


                "email":
                user.email,


                "parser":
                item.source,


                "pdf_count":
                item.pdf_count,


                "date":
                item.created_at

            })



    return result








# =====================================================
# DELETE USER
# =====================================================


@router.delete("/delete-user/{user_id}")
def delete_user(

    user_id:int,

    db:Session = Depends(get_db),

    admin=Depends(admin_required)

):


    user = db.query(
        User
    ).filter(

        User.id ==
        user_id

    ).first()



    if not user:


        raise HTTPException(

            status_code=404,

            detail="User not found"

        )




    # Admin cannot delete himself


    if user.id == admin.id:


        raise HTTPException(

            status_code=400,

            detail="Admin cannot delete own account"

        )





    # delete analytics

    db.query(

        UploadAnalytics

    ).filter(

        UploadAnalytics.user_id ==
        user.id

    ).delete()




    # delete OTP

    db.query(

        OTPCode

    ).filter(

        OTPCode.user_id ==
        user.id

    ).delete()





    # delete user


    db.delete(user)

    db.commit()



    return {


        "message":
        "User deleted successfully"


    }









# =====================================================
# UPLOAD STATS
# =====================================================


@router.get("/upload-stats")
def upload_stats(

    db:Session = Depends(get_db),

    admin=Depends(admin_required)

):


    data = db.query(

        UploadAnalytics.source,

        func.sum(
            UploadAnalytics.pdf_count
        )

    ).group_by(

        UploadAnalytics.source

    ).all()



    return [


        {

            "source":
            row[0],


            "pdf_count":
            row[1] or 0

        }


        for row in data

    ]