# Import necessary modules and classes from the 'utils' module
from utils import *

# Feedback mechanism for Answer Relevance
qa_relevance = (
    Feedback(openai.relevance_with_cot_reasons, name="Answer Relevance")
    .on_input_output()  # Apply feedback on both input and output
)

# Feedback mechanism for Context Relevance
qs_relevance = (
    Feedback(openai.relevance_with_cot_reasons, name="Context Relevance")
    .on_input()  # Apply feedback only on input
    .on(TruLlama.select_source_nodes().node.text)  # Select source nodes' text for feedback
    .aggregate(np.mean)  # Aggregate using the mean
)

# Groundedness feedback using the 'Groundedness' class from the 'utils' module
# Commented out options indicate possible alternatives or configurations
# grounded = Groundedness(groundedness_provider=openai, summarize_provider=openai)
grounded = Groundedness(groundedness_provider=openai)

# Feedback mechanism for Groundedness
groundedness = (
    Feedback(grounded.groundedness_measure_with_cot_reasons, name="Groundedness")
        .on(TruLlama.select_source_nodes().node.text)  # Apply feedback on source nodes' text
        .on_output()  # Apply feedback on the output
        .aggregate(grounded.grounded_statements_aggregator)  # Aggregate using a specific aggregator
)

# Create a list of feedback mechanisms for use in the RAG system
feedbacks = [qa_relevance, qs_relevance, groundedness]
