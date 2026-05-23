from pydantic import BaseModel


class JobCreate(

    BaseModel

):

    title:str

    experience:str

    skills:str

    description:str

    location:str

    salary:str

    openings:int

    deadline:str