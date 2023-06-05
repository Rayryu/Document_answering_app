from typing import List

import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from constants import (
    OPENAI_LLM_STR,
    OPENAI_EMBEDDING_STR,
    FLAN_LLM_STR,
    INSTRUCTOR_EMBEDDING_STR,
)
from html_templates import bot_template, user_template


def build_corpus(documents: List[str]) -> str:
    """
    Build a text corpus from a list of PDF documents.

    Args:
        documents (List[str]): List of document paths.

    Returns:
        str: Text corpus constructed from the documents.
    """
    corpus = ""
    for document in documents:
        pdf_reader = PdfReader(document)
        for page in pdf_reader.pages:
            corpus += page.extract_text()
    return corpus


def build_chunks(corpus: str):
    """
    Split the corpus into chunks of text.

    Args:
        corpus (str): Text corpus to be split.

    Returns:
        List[str]: List of text chunks split from the corpus.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[" ", ",", "\n"],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return text_splitter.split_text(corpus)


def build_knowledge_base(chunks, embeddings_type=INSTRUCTOR_EMBEDDING_STR):
    """
    Build a knowledge base from the chunks using the chosen embeddings.

    Args:
        chunks (List[str]): List of text chunks.
        embeddings_type (str): Type of embeddings to be used. Default is 'INSTRUCTOR_EMBEDDING_STR'.

    Returns:
        Knowledge base built from the chunks.
    """
    if embeddings_type == INSTRUCTOR_EMBEDDING_STR:
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    elif embeddings_type == OPENAI_EMBEDDING_STR:
        embeddings = OpenAIEmbeddings()

    return FAISS.from_texts(texts=chunks, embedding=embeddings)


def build_conversation_chain(knowledge_base, llm_type=FLAN_LLM_STR):
    """
    Build a conversation chain from the knowledge base.

    Args:
        knowledge_base (FAISS): The knowledge base to be used.
        llm_type (str): The type of language model to be used. Default is 'FLAN_LLM_STR'.

    Returns:
        ConversationalRetrievalChain: The conversation chain built from the knowledge base.
    """
    if llm_type == FLAN_LLM_STR:
        llm = HuggingFaceHub(
            repo_id="google/flan-t5-xxl",
            model_kwargs={"temperature": 0.5, "max_length": 512},
        )
    elif llm_type == OPENAI_LLM_STR:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=knowledge_base.as_retriever(), memory=memory
    )

    return conversation_chain


def handle_user_input(user_question):
    """
    Handle user input and write responses to the Streamlit page.

    Args:
        user_question (str): The user's question.
    """
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
