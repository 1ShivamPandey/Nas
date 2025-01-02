# import os
# import streamlit as st
# from PyPDF2 import PdfReader
# from langchain.chat_models import ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.docstore.document import Document
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize OpenAI API key
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# st.title("Nas Youtube")

# # Sidebar for document upload
# st.sidebar.title("Upload Documents")
# uploaded_files = st.sidebar.file_uploader(
#     "Upload one or more PDF files",
#     type="pdf",
#     accept_multiple_files=True
# )

# if uploaded_files:
#     def extract_text_from_pdfs(uploaded_files):
#         """Extract text content from uploaded PDF files."""
#         all_text = ""
#         for uploaded_file in uploaded_files:
#             pdf_reader = PdfReader(uploaded_file)
#             for page in pdf_reader.pages:
#                 all_text += page.extract_text()
#         return all_text

#     def split_text_into_documents(text, chunk_size=1000, overlap=200):
#         """Split long text into manageable chunks."""
#         chunks = []
#         for i in range(0, len(text), chunk_size - overlap):
#             chunk = text[i:i + chunk_size]
#             chunks.append(Document(page_content=chunk))
#         return chunks

#     st.info("Extracting text from PDFs...")
#     raw_text = extract_text_from_pdfs(uploaded_files)
#     st.success("Text extracted successfully!")

#     # Split text into chunks
#     st.info("Splitting text into smaller chunks...")
#     documents = split_text_into_documents(raw_text)
#     st.success(f"Text split into {len(documents)} chunks.")

#     # Ask questions
#     st.subheader("Ask questions about your PDFs:")
#     question = st.text_input("Enter your question:")

#     if question:
#         # Load QA chain
#         chain = load_qa_chain(llm, chain_type="stuff")
#         st.info("Fetching the answer...")

#         # Get the answer
#         # answer = chain.run(input_documents=documents, question=question)
#         # st.success(f"Answer: {answer}")
#         # 
#         answer = chain.run(input_documents=documents, question=question)

#         # Display the answer in a proper format
#         st.markdown("### Answer")
#         st.markdown(f"**Question:** {question}")
#         st.markdown(f"**Answer:** {answer}")

# else:
#     st.sidebar.info("Upload one or more PDF files to get started.")
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI API key

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


openai_api_key = st.secrets["OPENAI_API_KEY"]
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)


st.title("Nas Daily Youtube Assistant")

# Sidebar for document upload
st.sidebar.title("Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload one or more PDF files",
    type="pdf",
    accept_multiple_files=True
)

# Initialize session state for documents and chat history
if "documents" not in st.session_state:
    st.session_state.documents = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

    if not st.session_state.documents:
        st.info("Extracting text from PDFs...")
        raw_text = extract_text_from_pdfs(uploaded_files)
        st.success("Text extracted successfully!")

        # Split text into chunks
        st.info("Splitting text into smaller chunks...")
        st.session_state.documents = split_text_into_documents(raw_text)
        st.success(f"Text split into {len(st.session_state.documents)} chunks.")

# Display chat history
if st.session_state.chat_history:
    for message in st.session_state.chat_history:
        if message["type"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

# Input box at the bottom
if st.session_state.documents:
    question = st.chat_input("Ask your question or follow-up:")

    if question:
        # Add user's question to chat history
        st.session_state.chat_history.append({"type": "user", "content": question})
        st.chat_message("user").write(question)

        # Load QA chain
        chain = load_qa_chain(llm, chain_type="stuff")
        with st.spinner("Fetching the answer..."):
            answer = chain.run(input_documents=st.session_state.documents, question=question)

        # Add assistant's answer to chat history
        st.session_state.chat_history.append({"type": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
else:
    st.sidebar.info("Upload one or more PDF files to get started.")
