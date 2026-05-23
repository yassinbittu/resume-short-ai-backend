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

    candidate = db.query(

    Candidate

).filter(

    Candidate.id
    ==
    current_user[
        "candidate_id"
    ]

).first()


    if not job:

        return {

            "message":
            "Job Not Found"

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