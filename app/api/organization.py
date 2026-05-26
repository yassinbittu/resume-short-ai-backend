from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from schemas.organization_schema import OrganizationCreate

from core.database import get_db

from models.organization import Organization

from core.auth import superadmin_only

from core.security import hash_password

from services.email_service import (
    send_pending_mail,
    send_approval_mail
)

import uuid


router = APIRouter()


@router.post("/register")

async def register_organization(

        data: OrganizationCreate,

        db: Session = Depends(get_db)

):

    new_org = Organization(

        public_org_id = str(

        uuid.uuid4()

    ),

    org_name=
    data.org_name,

    admin_name=
    data.admin_name,

    email=
    data.email,

    password=
    hash_password(
        data.password
    ),

    website=
    data.website,

    industry=
    data.industry,

    max_applications =
    data.max_applications,
)


    db.add(new_org)

    db.commit()

    db.refresh(new_org)


    await send_pending_mail(
        data.email
    )


    return {

        "message":
        "Registration Submitted",

        "status":
        "Pending Approval"
    }


@router.get("/")

def get_organizations(

        current_user:
        dict=
        Depends(
            superadmin_only
        ),
        db: Session = Depends(get_db)
):

    organizations = db.query(
        Organization
    ).all()

    return organizations

@router.put("/approve/{org_id}")

async def approve_organization(
        org_id:int,

        current_user:
        dict=
        Depends(
            superadmin_only
        ),

        db:Session=Depends(get_db)
):

    organization=db.query(
        Organization
    ).filter(
        Organization.id==org_id
    ).first()


    if not organization:

        return {
            "message":
            "Organization not found"
        }


    organization.status="Approved"

    organization.org_code=(
        f"RSAI-ORG-{org_id:03d}"
    )

    db.commit()

    db.refresh(
        organization
    )


    await send_approval_mail(

        organization.email,

        organization.org_code
    )


    return {

        "message":
        "Approved",

        "org_code":
        organization.org_code
    }
