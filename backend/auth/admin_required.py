# backend/auth/admin_required.py


from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from auth.dependencies import get_current_user

from database.models import User



# =====================================================
# ADMIN ACCESS VALIDATION
# =====================================================

def admin_required(

    current_user: User = Depends(
        get_current_user
    )

):


    # =================================================
    # USER AUTHENTICATION CHECK
    # =================================================

    if current_user is None:


        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Authentication required"

        )



    # =================================================
    # ACTIVE ACCOUNT CHECK
    # =================================================

    if not current_user.is_active:


        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Account is inactive"

        )



    # =================================================
    # ADMIN ROLE CHECK
    # =================================================

    if not current_user.role:


        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Invalid user role"

        )



    if current_user.role.lower() != "admin":


        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Admin access required"

        )



    return current_user