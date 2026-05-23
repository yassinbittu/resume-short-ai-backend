from sqlalchemy import (

    Column,

    Integer,

    String

)

from core.database import Base


class Candidate(Base):

    __tablename__ = "candidates"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    public_candidate_id = Column(

        String,

        unique=True

    )


    email = Column(

        String,

        unique=True

    )


    password = Column(

        String

    )