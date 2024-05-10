import streamlit as st
import google.generativeai as genai

import PyPDF2 as pdf
import os

# api_key = os.getenv('GOOGLE_API_KEY')
# print("api", api_key)


genai.configure(api_key = os.environ.get('GOOGLE_API_KEY'))


# GEMINI PRO Responses

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = " "

    for page in reader(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text

# Prompt Template

prompt_template= """
Hey act like a skilled or very expensive ATS (Application Tracking system) 
with deep understanding of tech field, software engineering, data scienctist, data analyst and big data engineer.
your task is to evaluate resume based on given job description. You must consider the job market is very competitive and 
you should provide best assistance for impoving resume. Assign the percent matching based on the job description  
and missing keyword with high accuracy.

resume: {text}
desciption: {jd}

I want response in one single string with structure
{{"Job Description Match": "%", "Missing Keywords": [], "Profile Summary": ""}}

"""



# stramlit app

st.title("Smart ATS")
st.text = ("Improve your resume with ATS")
jd = st.text_area("Paste Job Description")
uploaded_file = st.file_uploader("Upload your resume", type ="pdf", help="Please upload the pdf file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(prompt_template)
        st.subheader(response)