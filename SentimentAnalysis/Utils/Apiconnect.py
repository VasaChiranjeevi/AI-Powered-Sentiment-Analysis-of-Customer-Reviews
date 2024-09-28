import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os
from  Utils.constant import MAX_ATTEMPTS
import logging
logger = logging.getLogger(__name__)
# Load environment variables from the .env file
load_dotenv()


 
def generate_response(prompt):
        """Generates a text response using the LLM based on the provided prompt"""
        attempts = 0
        max_retry = MAX_ATTEMPTS
        while attempts < max_retry:
            try:
                genai.configure(api_key=os.environ["GEMINI_API_KEY"])
                MODEL = os.getenv('MODEL')

                if not MODEL:
                    logger.error("MODEL environment variable is not set")
                    raise ValueError("MODEL environment variable is not set")

                model = genai.GenerativeModel(MODEL)
                response = model.generate_content(prompt)

                if response.text is None:
                    logger.warning(f"Attempt {attempts + 1}: Received None as response text")
                    attempts += 1
                    continue
                return response.text

            except Exception as e:
                logger.error(f"Error occurred during generate_response on attempt {attempts + 1}: {e}")
                attempts += 1
        raise Exception(f"Failed to generate a valid response after {max_retry} attempts")