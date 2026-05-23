from api.organization import router as org_router

from api.auth import router as auth_router

from api.jobs import router as jobs_router

from api.application import router as application_router

from api.candidate import router as candidate_router

from api.ai import router as ai_router

routes = [

    {
        "router":
        org_router,

        "prefix":
        "/organization",

        "tags":
        ["Organization"]
    },

    {
        "router":
        auth_router,

        "prefix":
        "/auth",

        "tags":
        ["Auth"]
    },

    {
        "router":
        jobs_router,

        "prefix":
        "/jobs",

        "tags":
        ["Jobs"]
    },

    {
        "router":
        application_router,

        "prefix":
        "/applications",

        "tags":
        ["Applications"]
    },

    {

    "router":
    candidate_router,

    "prefix":
    "/candidate",

    "tags":
    ["Candidates"]

    },

    {

    "router":
    ai_router,

    "prefix":
    "/ai",

    "tags":
    ["AI"]

    }

]