# Import necessary libraries and modules
from utils import *

# Function to retrieve the OpenAI API key from environment variables
def get_openai_api_key():
    # Load environment variables from the .env file
    _ = load_dotenv(find_dotenv())
    
    # Return the OpenAI API key from the environment
    return os.getenv("OPENAI_API_KEY")

# Function to retrieve the Hugging Face API key from environment variables
def get_hf_api_key():
    # Load environment variables from the .env file
    _ = load_dotenv(find_dotenv())
    
    # Return the Hugging Face API key from the environment
    return os.getenv("HUGGINGFACE_API_KEY")

# Create an instance of the OpenAI class
openai = OpenAI()

# Note: It seems like the 'OpenAI' class is assumed to be defined in the 'utils' module.

# The following code assumes that there are additional functionalities and classes
# defined in the 'utils' module, such as the 'OpenAI' class.

# It's important to check the 'utils' module for the definition of the 'OpenAI' class
# and other functionalities used in this script.

# Please make sure that the 'OpenAI' class and related functionalities are properly defined
# in the 'utils' module, or provide additional information about those components if needed.
