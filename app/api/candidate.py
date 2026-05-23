from fastapi import APIRouter

from sqlalchemy.orm import Session

from fastapi import Depends

from core.database import get_db

from schemas.candidate_schema import CandidateSignup

from models.candidate import Candidate

from core.security import hash_password

import uuid


router = APIRouter()


@router.post(
    "/signup"
)

def candidate_signup(

    data: CandidateSignup,

    db: Session = Depends(
        get_db
    )

):

    # EMAIL EXISTS

    candidate = db.query(

        Candidate

    ).filter(

        Candidate.email
        ==
        data.email

    ).first()


    if candidate:

        return {

            "message":
            "Email Already Exists"

        }


    # PASSWORD MATCH

    if (

        data.password
        !=
        data.confirm_password

    ):

        return {

            "message":
            "Password Not Match"

        }


    new_candidate = Candidate(

        public_candidate_id=
        str(
            uuid.uuid4()
        ),

        email=
        data.email,

        password=
        hash_password(
            data.password
        )

    )


    db.add(
        new_candidate
    )

    db.commit()


    return {

        "message":
        "Signup Successful"

    }

