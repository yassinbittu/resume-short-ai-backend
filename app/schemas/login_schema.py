from pydantic import BaseModel


class OrganizationLogin(

    BaseModel

):

    email:str

    password:str