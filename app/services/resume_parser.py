import pdfplumber

import pytesseract

from PIL import Image

import os


pytesseract.pytesseract.tesseract_cmd = (

r"C:\Program Files\Tesseract-OCR\tesseract.exe"

)


def extract_resume_text(

    file_path

):

    ext = os.path.splitext(

        file_path

    )[1].lower()


    text = ""


    # PDF

    if ext == ".pdf":


        with pdfplumber.open(

            file_path

        ) as pdf:


            for page in pdf.pages:


                page_text = page.extract_text()


                if page_text:


                    text += page_text


    # IMAGE

    elif ext in [

        ".png",

        ".jpg",

        ".jpeg"

    ]:


        img = Image.open(

            file_path

        )


        text = pytesseract.image_to_string(

            img

        )


    return text