from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your document")
    st.header("Ask your document 🤔")

    # Upload the document
    document = st.file_uploader(
        "Upload your pdf", type="pdf"
    )

    # Read the document
    if document is not None:
        pdf_reader = PdfReader(document)

        corpus = ""
        for page in pdf_reader.pages:
            corpus += page.extract_text()

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators=[" ", ",", "\n"],
            chunk_size=1000,  # characters
            chunk_overlap=200,  # use the latest 200 chunks of the previous chunk as starting point for the next chunk
            length_function=len,
        )
        chunks = text_splitter.split_text(corpus)

        # Create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Create user input field
        question = st.text_input("Ask a question to your document: ")
        if question:
            docs = knowledge_base.similarity_search(question)

            print(len(docs))

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=question)

            st.write(response)


if __name__ == "__main__":
    main()
