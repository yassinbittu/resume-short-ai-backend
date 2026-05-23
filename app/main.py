from fastapi import FastAPI

from swagger import swagger_config

from routes import routes


app = FastAPI(
    **swagger_config
)


for route in routes:

    app.include_router(

        route["router"],

        prefix=
        route["prefix"],

        tags=
        route["tags"]

    )


@app.get(
    "/",
    tags=["Home"]
)

def home():

    return {

        "message":
        "ResumeShort AI Running"

    }