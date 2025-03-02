from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_evaluation_categories(job_description):
    """
    Sends the job description to OpenAI and extracts evaluation categories.
    
    Args:
        job_description (str): The job description entered by the recruiter.
    
    Returns:
        list: A list of extracted evaluation categories (3-10 categories).
    """

    # OpenAI API Call
    response = client.chat.completions.create(model="gpt-4o",  # Ensure you're using an advanced model
    messages=[
        {"role": "system", "content": "You are an expert recruiter assistant. Given a job description, identify key evaluation categories that will be used for each applicant. You will eventually be asked to provide numerical proficiency scores for each category for each applicant you see. Remember, each category can be a maximum of 3 words."},
        {"role": "user", "content": f"Analyze the following job description and extract 3-10 key proficiency evaluation categories that will be required for this job description. Return a list of only the categories, with no additional text. Each category must not be more than 3 words. No numerical numbering required, just return the list.:\n\n{job_description}"}
    ],
    temperature=0.7,
    max_tokens=150)

    # Extract AI response text
    raw_text = response.choices[0].message.content.strip()

    # Convert response to list format
    categories = raw_text.split("\n")

    print(categories)
    categories = [category.strip("- ") for category in categories if category]  # Clean up bullet points

    return categories

def get_ai_question():
    """
    Generates a dynamic interview question using OpenAI.

    Returns:
        str: A new AI-generated interview question.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI interviewer. Generate a relevant question based on job-specific evaluation categories."},
            {"role": "user", "content": "Generate an intelligent interview question for an applicant applying for this role."}
        ],
        temperature=0.7,
        max_tokens=50
    )

    return response["choices"][0]["message"]["content"].strip()