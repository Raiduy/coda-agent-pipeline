import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the OpenAI client pointing to your LiteLLM Proxy instance
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "any-string-or-your-proxy-key"), 
    base_url=os.getenv("OPENAI_BASE_URL", "")  # Update this to match your LiteLLM proxy URL
)

text_to_embed = "Using LiteLLM to route our text embeddings seamlessly."

try:
    # Generate the embedding via LiteLLM
    response = client.embeddings.create(
        # The model name matches whatever identifier or alias you set up in your LiteLLM config
        model="Qwen3-Embedding-8B", 
        input=text_to_embed
    )
    
    # Extract the vector
    embedding_vector = response.data[0].embedding
    
    print(f"Embedding successfully fetched via LiteLLM!")
    print(f"Vector dimensions: {len(embedding_vector)}")
    print(f"First 3 dimensions: {embedding_vector[:3]}")

except Exception as e:
    print(f"An error occurred: {e}")
