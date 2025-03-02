import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def extract_evaluation_categories(job_description):
    """
    Sends the job description to OpenAI and extracts evaluation categories.
    
    Args:
        job_description (str): The job description entered by the recruiter.
    
    Returns:
        list: A list of extracted evaluation categories (3-10 categories).
    """

    # OpenAI API Call
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Ensure you're using an advanced model
        messages=[
            {"role": "system", "content": "You are an expert recruiter assistant. Given a job description, extract the key evaluation categories for screening applicants."},
            {"role": "user", "content": f"Analyze the following job description and extract 3-10 key evaluation categories:\n\n{job_description}"}
        ],
        temperature=0.7,
        max_tokens=150
    )

    # Extract AI response text
    raw_text = response["choices"][0]["message"]["content"].strip()

    # Convert response to list format
    categories = raw_text.split("\n")
    categories = [category.strip("-• ") for category in categories if category]  # Clean up bullet points

    return categories
