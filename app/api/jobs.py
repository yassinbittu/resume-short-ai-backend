from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from core.database import get_db

from core.auth import get_current_user

from models.job import Job

from models.organization import Organization

from schemas.job_schema import JobCreate

import uuid


router = APIRouter()


@router.post(
    "/create"
)

def create_job(

    data: JobCreate,

    current_user: dict = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    organization = db.query(
        Organization
    ).filter(

        Organization.id
        ==
        current_user[
            "org_id"
        ]

    ).first()


    new_job = Job(

        public_job_id = str(
            uuid.uuid4()
        ),

        org_id =
        organization.id,

        org_public_id =
        organization.public_org_id,

        title =
        data.title,

        experience =
        data.experience,

        skills =
        data.skills,

        description =
        data.description,

        location =
        data.location,

        salary =
        data.salary,

        openings =
        data.openings,

        deadline =
        data.deadline
    )


    db.add(
        new_job
    )

    db.commit()

    db.refresh(
        new_job
    )


    return {

        "message":
        "Job Created",

        "job_id":
        new_job.public_job_id

    }

@router.get(
    "/"
)

def get_jobs(

    current_user:
    dict = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    jobs = db.query(

        Job

    ).filter(

        Job.org_id
        ==
        current_user[
            "org_id"
        ]

    ).all()


    return jobs

@router.put(
    "/update/{job_id}"
)

def update_job(

    job_id:str,

    data:JobCreate,

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

    job = db.query(
        Job
    ).filter(

        Job.public_job_id
        ==
        job_id,

        Job.org_id
        ==
        current_user[
            "org_id"
        ]

    ).first()


    if not job:

        return {

            "message":
            "Job Not Found"

        }


    job.title = data.title

    job.experience = data.experience

    job.skills = data.skills

    job.description = data.description

    job.location = data.location

    job.salary = data.salary

    job.openings = data.openings

    job.deadline = data.deadline


    db.commit()

    db.refresh(
        job
    )


    return {

        "message":
        "Job Updated"

    }

@router.delete(
    "/delete/{job_id}"
)

def delete_job(

    job_id:str,

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

    job = db.query(
        Job
    ).filter(

        Job.public_job_id
        ==
        job_id,

        Job.org_id
        ==
        current_user[
            "org_id"
        ]

    ).first()


    if not job:

        return {

            "message":
            "Job Not Found"

        }


    db.delete(
        job
    )

    db.commit()


    return {

        "message":
        "Job Deleted"

    }

@router.put(
    "/close/{job_id}"
)

def close_job(

    job_id:str,

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

    job = db.query(
        Job
    ).filter(

        Job.public_job_id
        ==
        job_id,

        Job.org_id
        ==
        current_user[
            "org_id"
        ]

    ).first()


    if not job:

        return {

            "message":
            "Job Not Found"

        }


    job.status = "Closed"

    db.commit()


    return {

        "message":
        "Job Closed"

    }

