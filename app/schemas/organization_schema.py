from pydantic import BaseModel


class OrganizationCreate(BaseModel):

    org_name:str

    admin_name:str

    email:str

    password:str

    website:str

    industry:str

    max_applications:int