# Dependencies
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print the OpenAI library version to check
try:
    import openai
    print(f"OpenAI library version: {openai.__version__}")
except:
    print("Could not determine OpenAI library version")

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("API key not found in environment. Checking for alternative format in .env...")
    # Some people format their .env files differently, try to accommodate that
    with open('.env', 'r') as env_file:
        for line in env_file:
            if 'api_key' in line.lower():
                parts = line.split('=', 1)
                if len(parts) == 2:
                    api_key = parts[1].strip().strip('"').strip("'")
                    print("Found API key in alternative format")
                    break
    
    if not api_key:
        raise ValueError("API key not found. Make sure OPENAI_API_KEY is set in your .env file using format: OPENAI_API_KEY=your_key_here")

# Set API version environment variable
os.environ["OPENAI_API_VERSION"] = "2024-05-08"  # Using a recent API version

# Create client with the beta header explicitly set
client = OpenAI(
    api_key=api_key,
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

try:
    print("Attempting to create assistant...")
    
    # Create recruiter assistant and setup instructions
    response = client.beta.assistants.create(
        name="Recruiter Assistant",
        instructions="""
        You are a recruiter assistant. Your primary role is to assist recruiters in screening applicants based on job role requirements and proficiency criteria. 

        When the recruiter says "start screening", begin asking the applicant questions based on the job role and proficiency requirements provided. 

        When the recruiter says "end screening", provide an analysis of the applicant's responses, including both implicit and explicit insights.

        Job Role: {job_role_name}
        Description: {job_role_description}
        Proficiency Requirements: {proficiency_requirements}

        Please ask the applicant questions to ascertain their suitability for the role based on the above information.
        """,
        model="gpt-4-turbo",
        tools=[]  # Empty tools array for v2
    )

    # Save the assistant ID to use in other parts of the application
    ADMIN_ASSISTANT_ID = response.id
    print(f"Recruiter Assistant created with ID: {ADMIN_ASSISTANT_ID}")

except Exception as e:
    print(f"Error creating assistant: {str(e)}")
    print("\nTrying alternative approach...")
    
    # Try alternative approach with direct headers
    try:
        alt_client = OpenAI()
        alt_client.headers["OpenAI-Beta"] = "assistants=v2"
        
        response = alt_client.beta.assistants.create(
            name="Recruiter Assistant",
            instructions="You are a recruiter assistant...",  # Shortened for brevity
            model="gpt-4-turbo",
            tools=[]
        )
        
        ADMIN_ASSISTANT_ID = response.id
        print(f"Success with alternative approach! Assistant ID: {ADMIN_ASSISTANT_ID}")
    except Exception as alt_e:
        print(f"Alternative approach also failed: {str(alt_e)}")
        print("\nTroubleshooting tips:")
        print("1. Check that python-dotenv is installed: pip install python-dotenv")
        print("2. Make sure your .env file contains: OPENAI_API_KEY=your_key_here")
        print("3. Try upgrading the OpenAI library: pip install --upgrade openai")