# Import the load_dotenv function to load environment variables from a .env file
from dotenv import load_dotenv
# Import the ChatGoogleGenerativeAI class for interacting with Google's generative AI models
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from a .env file (e.g., API keys)
load_dotenv()

# Initialize the generative AI model with the specified model name
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Use the model to generate a response to the given prompt
result = llm.invoke("Write a professional LinkedIn post about learning AI agents.")
# Print the generated content to the console
print(result.content)