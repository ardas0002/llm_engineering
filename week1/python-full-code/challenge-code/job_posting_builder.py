from typing import Optional
from job_posting import JobPosting
from open_ai_client import OpenAIClient

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
```
"""

class JobPostingBuilder:

    def __init__(self, openai_client: OpenAIClient):
        self.openai = openai_client

    def create_job_posting_from_url(self, url: str) -> JobPosting:
        """Creates a JobPosting object from a URL by calling the OpenAI API."""
        response = self.openai.get_json_response(
            model="gpt-4",
            system_prompt=JOB_OFFER_SYSTEM_PROMPT,
            user_prompt=url
        )
        return self._serialize_to_job_posting(response)

    def _serialize_to_job_posting(self, data: dict) -> JobPosting:
        """Serializes the JSON response into a JobPosting object."""
        return JobPosting.from_dict(data)