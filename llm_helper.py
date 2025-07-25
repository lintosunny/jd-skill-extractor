import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variable
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY environment variable is not set.")

llm = ChatGroq(model_name="compound-beta", api_key=api_key)
parser = JsonOutputParser()
template = PromptTemplate.from_template(
    """
    You are an expert recruiter.
    
    Extract the key skills required from the following job description and assign each an importance score between 0 and 100.

    Total of all importance scores should be 100.
    
    Respond **only** in valid JSON format — no explanation, no preamble, no commentary.
    
    Format:
    [
      {{ "skill": "Skill Name", "importance": Number }},
      ...
    ]
    
    Job Description:
    {job_description}
    
    """)

def skill_extractor(job_description):
    """
    Extracts skills and their importance from a job description using an LLM.
    
    Args:
        job_description (str): The job description text.
        
    Returns:
        list: A list of dictionaries containing skills and their importance.
    """

    chain = template | llm
    response = chain.invoke({"job_description":job_description})
    output_json = parser.parse(response.content)
    return output_json