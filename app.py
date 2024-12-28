import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

st.title("📄 Chat with PDFs")
#st.sidebar.title("Configuration")

# openai_api_key = st.sidebar.text_input(
#     "Enter your OpenAI API Key:", type="password"
# )

# if not openai_api_key:
#     st.warning("Please enter your OpenAI API Key in the sidebar.")
# else:
#     os.environ["OPENAI_API_KEY"] = openai_api_key
#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type="pdf",
        accept_multiple_files=True
    )

if uploaded_files:
        def extract_text_from_pdfs(uploaded_files):
            """Extract text content from uploaded PDF files."""
            all_text = ""
            for uploaded_file in uploaded_files:
                pdf_reader = PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    all_text += page.extract_text()
            return all_text

        def split_text_into_documents(text, chunk_size=1000, overlap=200):
            """Split long text into manageable chunks."""
            chunks = []
            for i in range(0, len(text), chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                chunks.append(Document(page_content=chunk))
            return chunks

        st.info("Extracting text from PDFs...")
        raw_text = extract_text_from_pdfs(uploaded_files)
        st.success("Text extracted successfully!")

        # Split text into chunks
        st.info("Splitting text into smaller chunks...")
        documents = split_text_into_documents(raw_text)
        st.success(f"Text split into {len(documents)} chunks.")

        # Ask questions
        st.subheader("Ask questions about your PDFs:")
        question = st.text_input("Enter your question:")

        if question:
            # Load QA chain
            chain = load_qa_chain(llm, chain_type="stuff")
            st.info("Fetching the answer...")

            # Get the answer
            answer = chain.run(input_documents=documents, question=question)
            st.success(f"Answer: {answer}")
