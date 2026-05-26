from fastapi import (

    APIRouter,

    Depends

)

from sqlalchemy.orm import Session

from core.database import get_db

from models.application import Application

from models.job import Job

from services.resume_parser import (

    extract_resume_text

)

from services.ats_service import (

    calculate_ats

)


router = APIRouter()

@router.post(
    "/analyze/{application_id}"
)

def analyze_resume(

    application_id:str,

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


    job = db.query(

        Job

    ).filter(

        Job.id
        ==
        application.job_id

    ).first()


    resume_text = extract_resume_text(

        application.resume

    )


    jd_text = f"""

    {job.title}

    {job.skills}

    {job.description}

    {job.experience}

    """


    ats_score = calculate_ats(

        resume_text,

        jd_text

    )


    application.ats_score = ats_score


    if ats_score >= 70:

        application.decision = "Shortlisted"

        application.status = "Shortlisted"


    elif ats_score >= 50:

        application.decision = "Review"

        application.status = "Review"


    else:

        application.decision = "Rejected"

        application.status = "Rejected"


    shortlisted_count = db.query(

        Application

    ).filter(

        Application.job_id
        ==
        job.id,

        Application.status
        ==
        "Shortlisted"

    ).count()


    if shortlisted_count >= job.openings:

        job.status = "Closed"


    db.commit()


    return {

        "candidate":
        application.email,

        "ats_score":
        ats_score,

        "decision":
        application.decision,

        "job_status":
        job.status

    }
