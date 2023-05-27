import streamlit as st
from PyPDF2 import PdfReader


def main():
    st.set_page_config(page_title="Ask your document")
    st.header("Ask your document 🤔")

    # Upload the document
    document = st.file_uploader(
        "Upload your document", type="pdf"
    )  # TODO: I'll start with pdf then maybe add other types

    # Read the document
    if document is not None:
        pdf_reader = PdfReader(document)

        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()

        print(content)


if __name__ == "__main__":
    main()
