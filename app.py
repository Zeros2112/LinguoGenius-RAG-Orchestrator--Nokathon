from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from llama_index import SimpleDirectoryReader, Document, ServiceContext, VectorStoreIndex, load_index_from_storage
from llama_index.node_parser import HierarchicalNodeParser
from llama_index.llms import OpenAI
from llama_index.node_parser import HierarchicalNodeParser
from llama_index.node_parser import get_leaf_nodes
from llama_index import StorageContext, load_index_from_storage
from llama_index.retrievers import AutoMergingRetriever
from llama_index.indices.postprocessor import SentenceTransformerRerank
from llama_index.query_engine import RetrieverQueryEngine
import os

from llama_index import (
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)


app = Flask(__name__)
CORS(app)

# Create a variable to store the uploaded file path
uploaded_file_path = ""
documents = None
document = None
index = None
index2 = None

def build_automerging_index():
    global documents, document, index, index2

    # Check if 'documents' is None or empty
    if not uploaded_file_path or not os.path.isfile(uploaded_file_path):
        return jsonify({'error': 'Please upload a document first'})

    # Load the document
    documents = SimpleDirectoryReader(input_files=[uploaded_file_path]).load_data()
    document = Document(text="\n\n".join([doc.text for doc in documents]))

    # Build the auto-merging index with the specified chunk sizes
    index = build_automerging_index_helper([2048,512], save_dir="merging_index_0")
    index2 = build_automerging_index_helper([2048,512,128], save_dir="merging_index_1")

    return jsonify({'success': True})

def build_automerging_index_helper(chunk_sizes, save_dir):
    # Ensure 'document' is not None
    if not document:
        raise Exception('No document available')

    node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=chunk_sizes)
    nodes = node_parser.get_nodes_from_documents(documents)
    leaf_nodes = get_leaf_nodes(nodes)

    merging_context = ServiceContext.from_defaults(
        llm=OpenAI(model="gpt-3.5-turbo", temperature=0.1),
        embed_model="local:BAAI/bge-small-en-v1.5",
    )
    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(nodes)

    if not os.path.exists(save_dir):
        automerging_index = VectorStoreIndex(
            leaf_nodes, storage_context=storage_context, service_context=merging_context
        )
        automerging_index.storage_context.persist(persist_dir=save_dir)
    else:
        automerging_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=merging_context,
        )
    return automerging_index

def get_automerging_query_engine(auto_merging_index, similarity_top_k=12, rerank_top_n=6):
    base_retriever = auto_merging_index.as_retriever(similarity_top_k=similarity_top_k)
    retriever = AutoMergingRetriever(
        base_retriever, auto_merging_index.storage_context, verbose=True
    )
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )
    auto_merging_engine = RetrieverQueryEngine.from_args(
        retriever, node_postprocessors=[rerank]
    )
    return auto_merging_engine

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_document', methods=['POST'])
def upload_document():
    global uploaded_file_path, documents, document, index, index2

    # Check if 'file' is in request.files
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the file to the current working directory
    upload_folder = os.getcwd()  # Get the current working directory
    uploaded_file_path = os.path.join(upload_folder, secure_filename(file.filename))
    file.save(uploaded_file_path)

    # Build the auto-merging index
    build_automerging_index()

    return jsonify({'success': True})

@app.route('/generate_response', methods=['POST'])
def generate_response():
    global uploaded_file_path, documents, document, index, index2

    # Check if a document has been uploaded
    if not uploaded_file_path or not os.path.isfile(uploaded_file_path):
        return jsonify({'error': 'Please upload a document first'})


    question = request.form.get('question')


    # Get the query engines
    auto_merging_engine = get_automerging_query_engine(index, similarity_top_k=12, rerank_top_n=6)
    auto_merging_engine2 = get_automerging_query_engine(index2, similarity_top_k=12, rerank_top_n=6)

    # Query for the responses
    response = auto_merging_engine.query(question)
    response2 = auto_merging_engine2.query(question)

    return render_template('results.html', question=question, response=response, response2=response2)

if __name__ == '__main__':
    app.run(debug=True)
