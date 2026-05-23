from sqlalchemy import (

    Column,

    Integer,

    String,

    Text,

    ForeignKey

)

from core.database import Base

import uuid


class Job(Base):

    __tablename__ = "jobs"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    public_job_id = Column(

        String,

        unique=True

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


    title = Column(
        String
    )

    experience = Column(
        String
    )

    skills = Column(
        Text
    )

    description = Column(
        Text
    )

    location = Column(
        String
    )

    salary = Column(
        String
    )

    openings = Column(
        Integer
    )

    deadline = Column(
        String
    )

    status = Column(

        String,

        default="Active"

    )