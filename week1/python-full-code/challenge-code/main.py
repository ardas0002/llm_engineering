from open_ai_client import OpenAIClient
from job_posting_builder import JobPostingBuilder
from cv_analyzer import CVAnalyzer
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path, override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not (api_key and api_key.startswith("sk-proj-") and len(api_key) > 10):
    raise ValueError("API key missing or malformed. Check your .env file!")

MODEL = "gpt-4"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

JOB_OFFER_SYSTEM_PROMPT = """You are an assistant specialized in analyzing job postings for career advisors and candidate screening tools.

You will be given a link or the full text of a job posting.

Your task is to extract and structure the relevant information from the job offer, focusing on the following categories:

- Job Title
- Company Name (if available)
- Location (remote, hybrid, onsite + city)
- Employment Type (e.g. full-time, part-time, contract)
- Job Description Summary
- Required Skills and Technologies
- Preferred/Nice-to-have Skills
- Required Experience (in years or levels like "Junior", "Mid", "Senior")
- Education Level (if mentioned)
- Language Requirements (if mentioned)
- Benefits and Perks
- Application Deadline (if available)
- Link to original job posting (if provided)

Respond in **JSON format** using this example structure:

```json
{
  "job_title": "DevOps Engineer",
  "company_name": "TechCorp",
  "location": "Remote",
  "employment_type": "Full-time",
  "description_summary": "We're looking for a DevOps Engineer to manage CI/CD pipelines and cloud infrastructure.",
  "required_skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
  "preferred_skills": ["Terraform", "Python scripting"],
  "required_experience": "2+ years",
  "education_level": "Bachelor's degree in Computer Science or related field",
  "language_requirements": ["English - B2 or higher"],
  "benefits": ["Private health insurance", "Flexible hours", "Training budget"],
  "application_deadline": "2024-05-01",
  "original_url": "https://example.com/job/devops-engineer"
}

"""

user_prompt = "https://justjoin.it/job-offer/the-codest-devops-engineer-warszawa-devops"

if __name__ == "__main__":
    client = OpenAIClient(api_key)
    job_posting_builder = JobPostingBuilder(client)
    cv_analyzer = CVAnalyzer(client)
    
    # Example URL - you can change this to any job posting URL
    url = "https://justjoin.it/job-offer/the-codest-devops-engineer-warszawa-devops"
    
    # Create job posting from URL
    job_posting = job_posting_builder.create_job_posting_from_url(url)
    
    # Print the job posting details
    print("\nJob Posting Details:")
    print(f"Title: {job_posting.job_title}")
    print(f"Company: {job_posting.company_name}")
    print(f"Location: {job_posting.location}")
    print(f"Description: {job_posting.description_summary}")
    
    print("\nRequired Skills:")
    if job_posting.required_skills:
        for skill in job_posting.required_skills:
            print(f"- {skill}")
    else:
        print("- No required skills specified")
    
    print("\nPreferred Skills:")
    if job_posting.preferred_skills:
        for skill in job_posting.preferred_skills:
            print(f"- {skill}")
    else:
        print("- No preferred skills specified")

    # Get CV path from user
    
    # Analyze CV against job posting
    print("\nAnalyzing your CV against the job posting...")
    analysis = cv_analyzer.analyze_cv_against_job("....", job_posting)
    
    # Print analysis results
    print("\nCV Analysis Results:")
    print(f"Overall Fit: {analysis['overall_fit']}")
    
    print("\nStrengths:")
    for strength in analysis['strengths']:
        print(f"- {strength}")
    
    print("\nAreas for Improvement:")
    for area in analysis['areas_for_improvement']:
        print(f"- {area}")
    
    print("\nMissing Requirements:")
    for req in analysis['missing_requirements']:
        print(f"- {req}")
    
    print("\nRecommendations:")
    for rec in analysis['recommendations']:
        print(f"- {rec}")


