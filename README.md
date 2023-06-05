
# Ask Your Document

Ask Your Document is an interactive document exploration tool, crafted to bring sophisticated document retrieval and analysis at your fingertips. This application lets users upload multiple PDF documents and ask queries regarding their content, all in a user-friendly manner. Powered by OpenAI's text-davinci-003 model, Hugging Face's instructor-xl model, and the Langchain library, the tool parses, understands, and answers questions related to your documents content.

## Prerequisites
Please refer to the `requirements.txt` file for a full list of dependencies.

## Installation

1.  Clone the repository:

	`git clone https://github.com/Rayryu/Document_answering_app.git` 

2.  Navigate to the project directory:

	`cd Document_answering_app` 

3.  Install the required dependencies:

	`pip install -r requirements.txt` 

4. Create a `.env` file and add your OPENAI API key:
    `OPENAI_API_KEY = <YOUR_KEY>`
	`HUGGINGFACEHUB_API_TOKEN = <YOUR_KEY>`

## Usage

To run the application:

`streamlit run app.py` 

This will start the Streamlit server and the application will be accessible at `http://localhost:8501`.

## Application Walkthrough

1.  When the application is launched, you can upload your PDF document using the file uploader option.
2.  Once the PDF is uploaded, the application reads the document, extracts the text, and splits it into manageable chunks.
3.  Using the OpenAI or Instructor Embeddings, embeddings for each chunk are created and stored in a knowledge base.
4.  You can then type a question related to the documents content in the provided text input field.
5.  The application finds the chunks most similar to your question and uses a Language Learning Model (LLM) to generate a response.
6.  The answer to your question is displayed on the screen.
7. You can continue the discussion with your document in a chatbot-like conversation.
