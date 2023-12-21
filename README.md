Advanced RAG System with TruLens and Flask
This repository contains code for building an advanced Retrieval-Augmented Generation (RAG) system using TruLens, Flask, and related libraries.

Overview
The RAG system is designed to enhance document retrieval and generation based on user queries. It incorporates TruLens for feedback-driven evaluation, Flask for creating a web interface, and a merging index approach for efficient document retrieval.

Components

1. TruLens Setup
   Utilizes TruLens for feedback-driven evaluation of Answer Relevance, Context Relevance, and Groundedness.
   OpenAI and Hugging Face API keys are required and should be provided through environment variables.
2. Automerging Index
   Builds an automerging index to efficiently retrieve information from a set of documents.
   HierarchicalNodeParser is used to parse documents into hierarchical nodes.
   AutoMergingRetriever combines retrieval results for improved accuracy.
3. Flask Web Interface
   Implements a web interface using Flask for user interaction.
   Allows users to upload documents, build the automerging index, and query the system for responses.
   Usage
   Prerequisites
   Python 3.x
   Pip package manager
   Installation
   Clone the repository:

bash
Copy code
git clone https://github.com/your-username/advanced-rag-system.git
cd advanced-rag-system
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Running the Application
Set up environment variables:

Rename the .env.example file to .env.
Add your OpenAI and Hugging Face API keys to the .env file.
Run the Flask application:

bash
Copy code
python app.py
Access the web interface:

Open your browser and navigate to http://localhost:5000.

Web Interface
Home: Displays the main page with options to upload a document and build the automerging index.

Upload Document: Allows users to upload a document for processing.

Generate Response: Accepts user queries and provides responses based on the automerging index.

Contributors
Your Name
Another Contributor
Acknowledgements
Special thanks to TruLens for their powerful evaluation framework.
Flask for providing a robust web framework.
License
This project is licensed under the MIT License - see the LICENSE file for details.