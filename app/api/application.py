from fastapi import (

    APIRouter,

    Depends,

    UploadFile,

    File,

    Form

)
from services.email_service import (

    send_application_mail

)
from sqlalchemy.orm import Session

from core.database import get_db

from models.application import Application

from models.job import Job

from core.auth import get_current_user

from models.candidate import Candidate

from models.organization import Organization

import uuid

import shutil

import os


router = APIRouter()

@router.post(
    "/apply/{job_id}"
)
async def apply_job(

    job_id:str,

    current_user:
    dict=
    Depends(
        get_current_user
    ),

    phone:
    str=
    Form(...),

    address:
    str=
    Form(...),

    experience:
    str=
    Form(...),

    resume:
    UploadFile=
    File(...),

    db:Session=
    Depends(
        get_db
    )

):

    job = db.query(
        Job
    ).filter(
        Job.public_job_id
        ==
        job_id
    ).first()


    if not job:
        
        return {

        "message":

        "Job Not Found"

    }


    if job.status == "Closed":
        
        return {
            "message":
            
            "Job Closed"
            
        }

    candidate = db.query(
        Candidate
    ).filter(
        Candidate.id
        ==
        current_user[
            "candidate_id"
        ]
    ).first()


    organization = db.query(
        Organization
    ).filter(
        Organization.id
        ==
        job.org_id
    ).first()


    active_applications = db.query(
        Application
    ).filter(

        Application.org_id
        ==
        job.org_id,

        Application.candidate_id
        ==
        candidate.id,

       Application.status.in_(

    [

        "Active",

        "Pending",

        "Review",

        "Shortlisted",

        "Rejected"

    ]

)

    ).count()


    if active_applications >= organization.max_applications:

        return {

            "message":

            f"Maximum {organization.max_applications} applications allowed for this organization"

        }

    existing_application = db.query(

    Application

).filter(

    Application.job_id
    ==
    job.id,

    Application.candidate_id
    ==
    candidate.id,

    Application.status.notin_(

        [

            "Withdrawn",

            "Closed"

        ]

    )

).first()


    if existing_application:

        return {

            "message":

            "Already Applied"

        }
    



    file_path = (
        f"uploads/"
        f"{resume.filename}"
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )


    application = Application(

        public_application_id=
        str(
            uuid.uuid4()
        ),

        org_id=
        job.org_id,

        org_public_id=
        job.org_public_id,

        candidate_id=
        candidate.id,

        candidate_name=
        candidate.email,

        email=
        candidate.email,

        phone=
        phone,

        address=
        address,

        experience=
        experience,

        resume=
        file_path,

        job_id=
        job.id

    )


    db.add(
        application
    )

    db.commit()


    await send_application_mail(

        candidate.email,

        candidate.email,

        job.title

    )


    return {

        "message":
        "Application Submitted"

    }



@router.get(
    "/my-applications"
)
def my_applications(

    current_user:
    dict=
    Depends(
        get_current_user
    ),

    db:Session=
    Depends(
        get_db
    )

):

    applications = db.query(
        Application
    ).filter(

        Application.candidate_id
        ==
        current_user[
            "candidate_id"
        ]

    ).all()


    return applications



@router.get(
    "/organization"
)
def organization_applications(

    current_user:
    dict=
    Depends(
        get_current_user
    ),

    db:Session=
    Depends(
        get_db
    )

):

    if current_user.get(
        "role"
    ) != "admin":

        return {
            "message":
            "Admin Access Only"
        }


    applications = db.query(
        Application
    ).filter(

        Application.org_id
        ==
        current_user.get(
            "org_id"
        )

    ).all()


    return applications
    
@router.put(
    "/withdraw/{application_id}"
)

def withdraw_application(

    application_id:str,

    current_user:
    dict=
    Depends(
        get_current_user
    ),

    db:Session=
    Depends(
        get_db
    )

):

    application = db.query(

    Application

).filter(

    Application.public_application_id
    ==
    application_id,

    Application.candidate_id
    ==
    current_user.get(
        "candidate_id"
    )

).first()


    if not application:

        return {

            "message":

            "Application Not Found"

        }


    application.status = "Withdrawn"

    db.commit()


    return {

        "message":

        "Application Withdrawn"

    }

@router.put(
    "/close/{application_id}"
)

def close_application(

    application_id:str,

    current_user:
    dict=
    Depends(
        get_current_user
    ),

    db:Session=
    Depends(
        get_db
    )

):

    application = db.query(

        Application

    ).filter(

        Application.public_application_id
        ==
        application_id

    ).first()


    if not application:

        return {

            "message":

            "Application Not Found"

        }


    application.status = "Closed"


    db.commit()


    return {

        "message":

        "Application Closed"

    }