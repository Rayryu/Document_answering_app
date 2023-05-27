from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

def main():
    # Load environment variables
    load_dotenv()
    
    # Set Streamlit page configuration
    st.set_page_config(page_title="Ask your document")
    
    # Add a header to the page
    st.header("Ask your document 🤔")

    # File uploader for the user to upload their PDF
    document = st.file_uploader("Upload your pdf", type="pdf")

    # If a document is uploaded, proceed to process it
    if document is not None:
        # Create a PDF reader object
        pdf_reader = PdfReader(document)

        # Loop through each page in the PDF and extract the text
        corpus = ""
        for page in pdf_reader.pages:
            corpus += page.extract_text()

        # Initialise the text splitter with specified parameters
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[" ", ",", "\n"],  # Character separators for splitting the text
            chunk_size=1000,  # Size of each chunk in characters
            chunk_overlap=200,  # Overlap size between chunks in characters
            length_function=len,  # Function to determine the length of a chunk
        )

        # Split the text into chunks
        chunks = text_splitter.split_text(corpus)

        # Create embeddings for each chunk using OpenAI embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Create a field for the user to input their question
        question = st.text_input("Ask a question to your document: ")
        
        # If a question is entered, process it
        if question:
            # Search the knowledge base for documents similar to the question
            docs = knowledge_base.similarity_search(question)

            # Create an OpenAI text-davinci-003 LLM
            llm = OpenAI()

            # Load a question-answering chain
            chain = load_qa_chain(llm, chain_type="stuff")
            
            # Generate a response to the question using the selected docs
            with get_openai_callback() as callback:
                response = chain.run(input_documents=docs, question=question)
                print("cost:", callback)

            # Display the response on the page
            st.write(response)


if __name__ == "__main__":
    main()
