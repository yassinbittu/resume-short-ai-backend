from fastapi import Depends, HTTPException

from fastapi.security import (

    HTTPBearer,

    HTTPAuthorizationCredentials

)

from jose import jwt

from core.security import (

    SECRET_KEY,

    ALGORITHM

)


security = HTTPBearer()


def get_current_user(

    credentials:
    HTTPAuthorizationCredentials =

    Depends(
        security
    )

):

    token = (

        credentials
        .credentials

    )

    payload = jwt.decode(

        token,

        SECRET_KEY,

        algorithms=
        [ALGORITHM]

    )

    return payload



def superadmin_only(

    user:dict=

    Depends(
        get_current_user
    )

):

    if user.get(

        "role"

    ) != "superadmin":

        raise HTTPException(

            status_code=
            403,

            detail=
            "SuperAdmin Access Only"

        )

    return user