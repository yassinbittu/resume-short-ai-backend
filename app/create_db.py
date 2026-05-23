from core.database import engine, Base

from models.organization import Organization

from models.job import Job

from models.application import Application

from models.candidate import Candidate

Base.metadata.create_all(
    bind=engine
)

print(
    "Tables Created"
)