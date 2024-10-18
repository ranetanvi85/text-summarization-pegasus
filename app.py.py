import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader
from docx import Document

# Load summarization model from Hugging Face
summarizer = pipeline("summarization")

# Function to summarize text
def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Function to read PDF file content
def read_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to read DOCX file content
def read_docx(file):
    doc = Document(file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

# Streamlit UI
st.title("Text Summarization App")

# File uploader for PDF or Word documents
uploaded_file = st.file_uploader("Upload a PDF or Word Document", type=['pdf', 'docx'])
# Text area for manual input
user_input = st.text_area("Or enter your text here", "")

if uploaded_file:
    # Summarize the file content
    if uploaded_file.type == "application/pdf":
        pdf_text = read_pdf(uploaded_file)
        summarized_text = summarize_text(pdf_text)
        st.write("Summarized PDF content:")
        st.write(summarized_text)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        docx_text = read_docx(uploaded_file)
        summarized_text = summarize_text(docx_text)
        st.write("Summarized Word content:")
        st.write(summarized_text)

elif user_input:
    # Summarize the user input
    summarized_text = summarize_text(user_input)
    st.write("Summarized Text:")
    st.write(summarized_text)
