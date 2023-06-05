from constants import (
    OPENAI_EMBEDDING_STR,
    OPENAI_LLM_STR,
    FLAN_LLM_STR,
    INSTRUCTOR_EMBEDDING_STR,
)
from html_templates import css, bot_template, user_template
from helpers import (
    build_corpus,
    build_chunks,
    build_conversation_chain,
    build_knowledge_base,
    handle_user_input,
)

from dotenv import load_dotenv
import streamlit as st


def main():
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
            options=[OPENAI_EMBEDDING_STR, INSTRUCTOR_EMBEDDING_STR],
            index=1,
        )

        # Allow user to select a LLM from the list
        llm_choice = st.selectbox(
            "Select LLM to use",
            options=[OPENAI_LLM_STR, FLAN_LLM_STR],
            index=1,
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
                st.session_state.conversation = build_conversation_chain(
                    knowledge_base, llm_choice
                )


# Run the main function when the script is run
if __name__ == "__main__":
    main()
