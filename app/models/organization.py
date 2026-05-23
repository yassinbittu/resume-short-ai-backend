from sqlalchemy import Column, Integer, String

from core.database import Base


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    public_org_id = Column(

    String,

    unique=True

)

    org_code = Column(
        String,
        unique=True
    )

    org_name = Column(
        String,
        nullable=False
    )

    admin_name = Column(
        String
    )

    email = Column(
        String,
        unique=True
    )

    password = Column(
        String
    )

    website = Column(
        String
    )

    industry = Column(
        String
    )

    status = Column(
        String,
        default="Pending"
    )