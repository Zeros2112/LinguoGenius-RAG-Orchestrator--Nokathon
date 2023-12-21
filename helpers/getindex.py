# Import necessary modules and classes from the 'utils' module
from utils import *

# Function to get an automerging query engine for a given automerging index
def get_automerging_query_engine(
    automerging_index,
    similarity_top_k=12,
    rerank_top_n=2,
):
    # Create a base retriever from the automerging index with specified similarity top-k
    base_retriever = automerging_index.as_retriever(similarity_top_k=similarity_top_k)
    
    # Create an AutoMergingRetriever using the base retriever and storage context
    # Verbose is set to True for additional output information
    retriever = AutoMergingRetriever(
        base_retriever, automerging_index.storage_context, verbose=True
    )
    
    # Create a SentenceTransformerRerank with specified rerank top-n and model
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )
    
    # Create a RetrieverQueryEngine with the retriever and rerank postprocessor
    auto_merging_engine = RetrieverQueryEngine.from_args(
        retriever, node_postprocessors=[rerank]
    )
    
    # Return the built automerging query engine
    return auto_merging_engine

