from pydantic import BaseModel


class ApplyJob(

    BaseModel

):

    candidate_name:str

    email:str

    phone:str

    address:str

    experience:str