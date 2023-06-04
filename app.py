from html_templates import css, bot_template, user_template

from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub


def build_corpus(documents):
    """Build a text corpus from a list of PDF documents"""
    corpus = ""
    for document in documents:
        pdf_reader = PdfReader(document)
        for page in pdf_reader.pages:
            corpus += page.extract_text()

    return corpus


def build_chunks(corpus):
    """Split the corpus into chunks of text"""
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[" ", ",", "\n"],  # Character separators for splitting the text
        chunk_size=1000,  # Size of each chunk in characters
        chunk_overlap=200,  # Overlap size between chunks in characters
        length_function=len,  # Function to determine the length of a chunk
    )

    return text_splitter.split_text(corpus)


def build_knowledge_base(chunks, embeddings_type="Instruct"):
    """Build a knowledge base from the chunks using the chosen embeddings"""
    if embeddings_type == "Instruct (Free but Slow)":
        embeddings = OpenAIEmbeddings()
    elif embeddings_type == "OpenAI (Paid and Fast)":
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

    return FAISS.from_texts(chunks, embeddings)


def build_conversation_chain(knowledge_base):
    """Build a conversation chain from the knowledge base"""
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl",
        model_kwargs={"temperature": 0.5, "max_length": 512},
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=knowledge_base.as_retriever(), memory=memory
    )

    return conversation_chain


def handle_user_input(user_question):
    """Handle user input and write responses to the Streamlit page"""
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )


def main():
    """Main function"""
    # Load environment variables
    load_dotenv()

    # Set Streamlit page configuration
    st.set_page_config(page_title="Ask your document")
    st.write(css, unsafe_allow_html=True)

    # Initialize session variables
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Add a header to the page
    st.header("Ask questions about your documents 🤔")

    # Create a text input for user questions
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question)

    # Create a sidebar for document upload and knowledge base selection
    with st.sidebar:
        st.subheader("Your documents set")

        # Allow user to upload multiple documents
        documents = st.file_uploader(
            "Upload your documents and click on 'Process'", accept_multiple_files=True
        )

        # Allow user to select a type of knowledge base embeddings
        knowledge_base_choice = st.selectbox(
            "Select Knowledge Base Embeddings",
            options=["OpenAI (Paid and Fast)", "Instruct (Free but Slow)"],
            index=1,  # default selection is 'Instruct'
        )

        # Process uploaded documents when 'Process' button is clicked
        if st.button("Process"):
            with st.spinner("Processing..."):
                # Build corpus from uploaded documents
                corpus = build_corpus(documents)

                # Split the corpus into chunks
                chunks = build_chunks(corpus)

                # Build a knowledge base from the chunks using the selected embeddings
                knowledge_base = build_knowledge_base(
                    chunks, embeddings_type=knowledge_base_choice
                )

                # Build a conversation chain from the knowledge base
                st.session_state.conversation = build_conversation_chain(knowledge_base)


# Run the main function when the script is run
if __name__ == "__main__":
    main()
