import streamlit as st
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from PyPDF2 import PdfReader
from docx import Document

# Load the Pegasus model and tokenizer
model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

# Function to summarize text
def summarize_text(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

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
st.title("Text Summarization App with Pegasus")

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
