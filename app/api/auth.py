from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from core.database import get_db

from models.organization import Organization

from models.candidate import Candidate

from schemas.login_schema import OrganizationLogin

from core.security import (

    verify_password,

    create_access_token

)


router = APIRouter()


@router.post(
    "/login"
)

def login(

    data: OrganizationLogin,

    db: Session = Depends(
        get_db
    )

):

    # ==========================
    # SUPERADMIN LOGIN
    # ==========================

    if (

        data.email
        ==
        "super@gmail.com"

        and

        data.password
        ==
        "super123"

    ):

        token = create_access_token(

            {

                "role":
                "superadmin"

            }

        )


        return {

            "message":
            "Login Successful",

            "role":
            "superadmin",

            "access_token":
            token

        }


    # ==========================
    # ADMIN LOGIN
    # ==========================

    organization = db.query(

        Organization

    ).filter(

        Organization.email
        ==
        data.email

    ).first()


    if organization:


        if not verify_password(

            data.password,

            organization.password

        ):

            return {

                "message":
                "Invalid Password"

            }


        if organization.status != "Approved":

            return {

                "message":
                "Wait for approval"

            }


        token = create_access_token(

            {

                "role":
                "admin",

                "email":
                organization.email,

                "org_id":
                organization.id

            }

        )


        return {

            "message":
            "Login Successful",

            "role":
            "admin",

            "admin_name":
            organization.admin_name,

            "organization":
            organization.org_name,

            "org_code":
            organization.org_code,

            "access_token":
            token

        }


    # ==========================
    # CANDIDATE LOGIN
    # ==========================

    candidate = db.query(

        Candidate

    ).filter(

        Candidate.email
        ==
        data.email

    ).first()


    if candidate:


        if not verify_password(

            data.password,

            candidate.password

        ):

            return {

                "message":
                "Invalid Password"

            }


        token = create_access_token(

            {

                "role":
                "candidate",

                "candidate_id":
                candidate.id

            }

        )


        return {

            "message":
            "Login Successful",

            "role":
            "candidate",

            "access_token":
            token

        }


    return {

        "message":
        "Invalid Email"

    }