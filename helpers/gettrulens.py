# Import necessary modules and classes from the 'utils' module
from utils import *

# Function to get a TruLens recorder with specified parameters
def get_trulens_recorder(query_engine, feedbacks, app_id):
    # Create an instance of TruLlama with the provided query engine, app ID, and feedback mechanisms
    tru_recorder = TruLlama(
        query_engine,
        app_id=app_id,
        feedbacks=feedbacks
    )
    # Return the TruLens recorder instance
    return tru_recorder

# Function to get a prebuilt TruLens recorder with specified parameters
def get_prebuilt_trulens_recorder(query_engine, app_id):
    # Note: 'feedbacks' is assumed to be a globally defined variable, as it is not passed as an argument.
    # If it's not defined globally, this function may raise an error.
    
    # Create an instance of TruLlama with the provided query engine, app ID, and pre-defined feedback mechanisms
    tru_recorder = TruLlama(
        query_engine,
        app_id=app_id,
        feedbacks=feedbacks  # Assuming 'feedbacks' is defined globally or in an accessible scope
    )
    # Return the prebuilt TruLens recorder instance
    return tru_recorder
