from typing import Optional
import PyPDF2
from open_ai_client import OpenAIClient
from job_posting import JobPosting

class CVAnalyzer:
    def __init__(self, openai_client: OpenAIClient):
        self.openai = openai_client

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def analyze_cv_against_job(self, cv_path: str, job_posting: JobPosting) -> dict:
        """Analyze a CV against a job posting and provide feedback."""
        # Extract text from CV (handles both PDF and text files)
        if cv_path.lower().endswith('.pdf'):
            cv_text = self.extract_text_from_pdf(cv_path)
        else:
            with open(cv_path, 'r', encoding='utf-8') as file:
                cv_text = file.read()

        # Create a prompt for GPT to analyze the CV against the job posting
        system_prompt = """You are an expert career advisor and CV analyzer. 
        Your task is to analyze a CV against a specific job posting and provide detailed feedback.
        
        Consider the following aspects:
        1. Required skills match
        2. Preferred skills match
        3. Experience level
        4. Education requirements
        5. Overall fit for the position
        
        Provide your analysis in JSON format with the following structure:
        {
            "overall_fit": "percentage or rating",
            "strengths": ["list of strengths"],
            "areas_for_improvement": ["list of areas that need improvement"],
            "missing_requirements": ["list of missing requirements"],
            "recommendations": ["list of specific recommendations"]
        }
        """

        user_prompt = f"""Job Posting Details:
        Title: {job_posting.job_title}
        Company: {job_posting.company_name}
        Required Skills: {', '.join(job_posting.required_skills)}
        Preferred Skills: {', '.join(job_posting.preferred_skills)}
        Required Experience: {job_posting.required_experience}
        Education Level: {job_posting.education_level}

        CV Content:
        {cv_text}

        Please analyze this CV against the job posting and provide detailed feedback.
        """

        # Get analysis from GPT
        analysis = self.openai.get_json_response(
            model="gpt-4",
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        return analysis 