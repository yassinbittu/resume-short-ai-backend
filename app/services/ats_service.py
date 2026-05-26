from sentence_transformers import (

    SentenceTransformer

)

from sklearn.metrics.pairwise import (

    cosine_similarity

)

import re


model = SentenceTransformer(

    "all-MiniLM-L6-v2"

)


def similarity_score(

    text1,

    text2

):

    emb1 = model.encode(

        text1

    )


    emb2 = model.encode(

        text2

    )


    score = cosine_similarity(

        [

            emb1

        ],

        [

            emb2

        ]

    )[0][0]


    return float(

        score

    )


def extract_keywords(

    text

):

    words = re.findall(

        r"\b[a-zA-Z0-9+#.]+\b",

        text.lower()

    )


    stop_words = {

        "and",

        "or",

        "the",

        "with",

        "for",

        "of",

        "to",

        "in",

        "we",

        "are",

        "looking",

        "candidate",

        "experience"

    }


    keywords = [

        w

        for w in words

        if len(w) > 2

        and w not in stop_words

    ]


    return list(

        set(
            keywords
        )

    )


def calculate_ats(

    resume_text,

    jd_text

):

    resume_text = resume_text.lower()

    jd_text = jd_text.lower()


    semantic_score = similarity_score(

        resume_text,

        jd_text

    )


    jd_keywords = extract_keywords(

        jd_text

    )


    matched = sum(

        1

        for word in jd_keywords

        if word in resume_text

    )


    keyword_score = (

        matched

        /

        max(

            len(
                jd_keywords
            ),

            1

        )

    )


    final_score = (

        semantic_score * 0.7

        +

        keyword_score * 0.3

    ) * 100


    return round(

        float(
            final_score
        ),

        2

    )