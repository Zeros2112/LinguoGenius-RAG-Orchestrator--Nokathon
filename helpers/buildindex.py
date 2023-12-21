# Import necessary modules and classes from the 'utils' module
from utils import *

# Function to build an automerging index for a set of documents
def build_automerging_index(
    documents,
    llm,
    embed_model="local:BAAI/bge-small-en-v1.5",
    save_dir="merging_index",
    chunk_sizes=None,
):
    # Set default chunk sizes if not provided
    chunk_sizes = chunk_sizes or [2048, 512, 128]
    
    # Create a hierarchical node parser with default chunk sizes
    node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=chunk_sizes)
    
    # Obtain hierarchical nodes from the provided documents
    nodes = node_parser.get_nodes_from_documents(documents)
    
    # Get leaf nodes from the hierarchical nodes
    leaf_nodes = get_leaf_nodes(nodes)
    
    # Create a service context for merging with specified language model and embedding model
    merging_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )
    
    # Create a storage context with default settings
    storage_context = StorageContext.from_defaults()
    
    # Add documents to the document store within the storage context
    storage_context.docstore.add_documents(nodes)

    # Check if the save directory exists
    if not os.path.exists(save_dir):
        # If the directory doesn't exist, create a new vector store index
        automerging_index = VectorStoreIndex(
            leaf_nodes, storage_context=storage_context, service_context=merging_context
        )
        # Persist the index to the specified directory
        automerging_index.storage_context.persist(persist_dir=save_dir)
    else:
        # If the directory exists, load the index from the storage context
        automerging_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=merging_context,
        )
    
    # Return the built automerging index
    return automerging_index
