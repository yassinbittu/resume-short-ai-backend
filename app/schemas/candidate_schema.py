from pydantic import BaseModel


class CandidateSignup(

    BaseModel

):

    email:str

    password:str

    confirm_password:str