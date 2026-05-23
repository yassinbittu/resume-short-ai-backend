import re


def calculate_ats(

    resume_text,

    jd_text

):

    resume_text = resume_text.lower()

    jd_text = jd_text.lower()


    jd_words = set(

        re.findall(

            r"\b[a-zA-Z+#.]+\b",

            jd_text

        )

    )


    resume_words = set(

        re.findall(

            r"\b[a-zA-Z+#.]+\b",

            resume_text

        )

    )


    matched = jd_words.intersection(

        resume_words

    )


    score = (

        len(
            matched
        )

        /

        len(
            jd_words
        )

    ) * 100


    return round(

        score,

        2

    )