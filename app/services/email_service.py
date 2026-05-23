from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from dotenv import load_dotenv

import os


load_dotenv("../.env")


conf = ConnectionConfig(

    MAIL_USERNAME=os.getenv(
        "MAIL_USERNAME"
    ),

    MAIL_PASSWORD=os.getenv(
        "MAIL_PASSWORD"
    ),

    MAIL_FROM=os.getenv(
        "MAIL_FROM"
    ),

    MAIL_PORT=int(
        os.getenv(
            "MAIL_PORT"
        )
    ),

    MAIL_SERVER=os.getenv(
        "MAIL_SERVER"
    ),

    MAIL_STARTTLS=True,

    MAIL_SSL_TLS=False,

    USE_CREDENTIALS=True
)

# from platform owner organization sending pending mail

async def send_pending_mail(
    email:str
):

    message = MessageSchema(

        subject=
        "Registration Received - ResumeShort AI",

        recipients=[email],

        body="""
Thank you for registering with ResumeShort AI.

Your organization registration is under review.

Please wait for approval.
""",

        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(
        message
    )

async def send_approval_mail(
    email:str,
    org_code:str
):

    message = MessageSchema(

        subject=
        "Organization Approved - ResumeShort AI",

        recipients=[email],

        body=f"""
Congratulations!

Your organization registration has been approved by the ResumeShort AI Team.

Organization Code:
{org_code}

You can now login and start posting jobs.

Thank you for choosing ResumeShort AI.

Regards,
ResumeShort AI Team
""",

        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(
        message
    )

# from orginzation sending mail to candatites

async def send_application_mail(

    email,

    candidate_name,

    title

):

    message = MessageSchema(

        subject=
        "Application Received - ResumeShort AI",

        recipients=
        [email],

        body=f"""

Hello {candidate_name},

Thank you for applying for the position:

{title}

Your application has been received successfully.

Our recruitment team will review your profile and resume.

You will receive further updates shortly.

Regards,
ResumeShort AI Team

""",

        subtype=
        "plain"

    )


    fm = FastMail(
        conf
    )

    await fm.send_message(
        message
    )