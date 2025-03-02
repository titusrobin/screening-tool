# Dependencies
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure OPENAI_API_KEY is set in your .env file")

# Create client with the beta header explicitly set
client = OpenAI(
    api_key=api_key,
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

def create_recruiter_assistant(job_role, job_description):
    """
    Creates a recruiter assistant that can analyze job descriptions and conduct screenings.
    
    Args:
        job_role (str): The title of the job role
        job_description (str): The detailed description of the job
        
    Returns:
        dict: Contains assistant_id, thread_id, and proficiencies list
    """
    # First, analyze the job description to extract proficiencies
    proficiencies = extract_proficiencies(job_role, job_description)
    
    # Create the assistant with the analyzed proficiencies
    assistant = client.beta.assistants.create(
        name=f"Recruiter Assistant - {job_role}",
        instructions=f"""
        You are an advanced recruiter assistant specialized in the {job_role} position.
        
        Your responsibilities include:
        
        1) UNDERSTANDING THE ROLE:
           Job Role: {job_role}
           Description: {job_description}
           
        2) KEY PROFICIENCIES REQUIRED:
           {json.dumps(proficiencies, indent=2)}
        
        3) SCREENING PROCESS:
           - When the recruiter says "start screening [number]", begin asking the candidate targeted questions
           - If a number is specified, ask that many questions, otherwise ask 5 questions
           - Ask questions that assess the key proficiencies identified for this role
           - Ask one question at a time and wait for a response
           - Structure questions to evaluate both technical skills and behavioral attributes
           
        4) ANALYSIS:
           - When the recruiter says "end screening", analyze all the candidate's responses
           - Provide an evaluation that includes:
              * Assessment of candidate's proficiency in each key area (score 1-10)
              * Identified strengths and improvement areas
              * Overall recommendation: Not Suitable, Potential Match, Strong Match
              
        Keep your tone professional and supportive throughout the process.
        """,
        model="gpt-4-turbo",
        tools=[]
    )
    
    # Create a thread for the conversation
    thread = client.beta.threads.create()
    
    # Return the IDs and proficiency data
    return {
        "assistant_id": assistant.id,
        "thread_id": thread.id,
        "proficiencies": proficiencies
    }

def extract_proficiencies(job_role, job_description):
    """
    Analyzes the job description to extract key proficiencies.
    
    Args:
        job_role (str): The title of the job role
        job_description (str): The detailed description of the job
        
    Returns:
        list: List of key proficiencies required for the job
    """
    system_prompt = """
    You are an expert job analyst. Extract 5-8 key proficiencies/skills required for the job role and description provided.
    Return your response as a JSON list of these proficiencies without scores or additional information.
    Example: ["Python Programming", "Database Management", "Communication Skills", "System Design", "CI/CD"]
    """
    
    # Send chat completion request for analysis
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Job Role: {job_role}\n\nDescription: {job_description}\n\nPlease respond with a JSON list of key proficiencies."}
        ],
        response_format={"type": "json_object"}
    )
    
    # Extract and return just the list of proficiencies
    result = json.loads(response.choices[0].message.content)
    
    # Handle the case where the API might return a dictionary
    if isinstance(result, dict) and "proficiencies" in result:
        return result["proficiencies"]
    elif isinstance(result, list):
        return result
    elif isinstance(result, dict):
        return list(result.keys())
    else:
        # Try to parse as a list if it's a different format
        try:
            return json.loads(result)
        except:
            return ["Error extracting proficiencies"]

def send_message(thread_id, assistant_id, message):
    """
    Sends a message to the assistant and returns the response.
    
    Args:
        thread_id (str): ID of the conversation thread
        assistant_id (str): ID of the assistant
        message (str): Message to send to the assistant
        
    Returns:
        str: Assistant's response
    """
    # Add the message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )
    
    # Create a run to process the message
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    
    # Wait for the run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        
        if run_status.status == "completed":
            break
            
        elif run_status.status in ["failed", "cancelled", "expired"]:
            return f"Error: Run {run_status.status}. Please try again."
    
    # Retrieve the assistant's response
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    
    # Get the most recent assistant message
    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value
    
    return "No response received."

# Example of how to use these functions
if __name__ == "__main__":
    # This is just a demonstration - your Streamlit app would call these functions
    job_role = "Senior Python Developer"
    job_description = """
    We are looking for a Senior Python Developer with 5+ years of experience to join our team.
    The ideal candidate will have strong experience with Django, FastAPI, and database design.
    Knowledge of cloud services (AWS/GCP) and CI/CD pipelines is required.
    The role involves architecting and implementing scalable backend systems.
    """
    
    # Create the assistant
    assistant_data = create_recruiter_assistant(job_role, job_description)
    
    print(f"Assistant created with ID: {assistant_data['assistant_id']}")
    print("Key proficiencies identified:")
    for skill in assistant_data['proficiencies']:
        print(f"- {skill}")
    
    # Example of sending messages (your Streamlit app would handle this)
    thread_id = assistant_data["thread_id"]
    assistant_id = assistant_data["assistant_id"]
    
    response = send_message(thread_id, assistant_id, "start screening 3")
    print(f"\nAssistant: {response}")