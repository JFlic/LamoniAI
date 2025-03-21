import os
from huggingface_hub import login

# Set the environment variable (you can also set this outside the script)
key = os.getenv("HUGGING_FACE_KEY25")

# Login using the token from environment variable
login(token_or_path=key)