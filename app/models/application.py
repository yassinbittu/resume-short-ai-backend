from sqlalchemy import (

    Column,

    Integer,

    Float,

    String,

    ForeignKey

)

from core.database import Base


class Application(Base):

    __tablename__ = "applications"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    public_application_id = Column(

        String,

        unique=True

    )

    candidate_id = Column(

    Integer,

    ForeignKey(

        "candidates.id"

    )

)


    org_id = Column(

        Integer,

        ForeignKey(

            "organizations.id"

        )

    )


    org_public_id = Column(

        String

    )


    candidate_name = Column(
        String
    )

    email = Column(
        String
    )

    phone = Column(
        String
    )

    address = Column(
        String
    )

    experience = Column(
        String
    )

    resume = Column(
        String
    )


    job_id = Column(

        Integer,

        ForeignKey(
            "jobs.id"
        )

    )


    status = Column(

        String,

        default="Pending"

    )


    ats_score = Column(

    Float,

    default=0

)


    decision = Column(

        String,

        default="Pending"

    )