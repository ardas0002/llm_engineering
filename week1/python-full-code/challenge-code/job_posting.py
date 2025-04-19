from dataclasses import dataclass
from typing import List, Optional

@dataclass
class JobPosting:
    job_title: Optional[str]
    company_name: Optional[str]
    location: Optional[str]
    employment_type: Optional[str]
    description_summary: Optional[str]
    required_skills: List[str]
    preferred_skills: List[str]
    required_experience: Optional[str]
    education_level: Optional[str]
    language_requirements: List[str]
    benefits: List[str]
    application_deadline: Optional[str]
    original_url: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            job_title=data.get("job_title"),
            company_name=data.get("company_name"),
            location=data.get("location"),
            employment_type=data.get("employment_type"),
            description_summary=data.get("description_summary"),
            required_skills=data.get("required_skills", []),
            preferred_skills=data.get("preferred_skills", []),
            required_experience=data.get("required_experience"),
            education_level=data.get("education_level"),
            language_requirements=data.get("language_requirements", []),
            benefits=data.get("benefits", []),
            application_deadline=data.get("application_deadline"),
            original_url=data.get("original_url")
        )


