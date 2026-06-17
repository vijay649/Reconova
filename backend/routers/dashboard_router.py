# backend/routers/dashboard_router.py


from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import desc


from database.database import get_db

from database.models import (
    UploadAnalytics,
    User
)

from auth.dependencies import get_current_user



router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"]

)





# =====================================================
# CURRENT USER PROFILE
# =====================================================


@router.get("/me")
def get_me(

    current_user: User = Depends(
        get_current_user
    )

):


    return {


        "id":
        current_user.id,


        "name":
        current_user.name,


        "email":
        current_user.email,


        "role":
        current_user.role,


        "is_verified":
        current_user.is_verified,


        "is_active":
        current_user.is_active,


        "created_at":
        current_user.created_at,


        "last_login":
        current_user.last_login

    }






# =====================================================
# TOTAL UPLOAD COUNT
# =====================================================


@router.get("/my-total-uploads")
def my_total_uploads(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):


    total = db.query(

        func.sum(
            UploadAnalytics.pdf_count
        )

    ).filter(

        UploadAnalytics.user_id ==
        current_user.id

    ).scalar()



    return {

        "total_uploads":
        total or 0

    }







# =====================================================
# SOURCE ANALYTICS
# =====================================================


@router.get("/my-source-analytics")
def my_source_analytics(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):


    result = db.query(

        UploadAnalytics.source,

        func.sum(
            UploadAnalytics.pdf_count
        )


    ).filter(


        UploadAnalytics.user_id ==
        current_user.id


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


        for row in result

    ]








# =====================================================
# DASHBOARD SUMMARY
# =====================================================


@router.get("/summary")
def dashboard_summary(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):


    result = db.query(

        UploadAnalytics.source,

        func.sum(
            UploadAnalytics.pdf_count
        )

    ).filter(

        UploadAnalytics.user_id ==
        current_user.id

    ).group_by(

        UploadAnalytics.source

    ).all()



    summary = {

        "amazon":0,

        "swiggy":0,

        "zomato":0,

        "blinkit":0,

        "flipkart":0

    }



    for source,count in result:


        if source in summary:

            summary[source] = count or 0




    summary["total_uploads"] = sum(
        summary.values()
    )



    return summary







# =====================================================
# RECENT USER ACTIVITY
# =====================================================


@router.get("/recent-activity")
def recent_activity(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):


    activities = db.query(

        UploadAnalytics

    ).filter(

        UploadAnalytics.user_id ==
        current_user.id

    ).order_by(

        desc(
            UploadAnalytics.created_at
        )

    ).limit(10).all()



    return [

        {

            "parser":
            item.source,


            "pdf_count":
            item.pdf_count,


            "date":
            item.created_at

        }


        for item in activities

    ]