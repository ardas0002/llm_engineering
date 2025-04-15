import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# === Config & Environment ===
load_dotenv(override=True)
env_path = Path(__file__).resolve().parents[2] / ".env"
api_key = os.getenv("OPENAI_API_KEY")

if not (api_key and api_key.startswith("sk-proj-") and len(api_key) > 10):
    raise ValueError("API key missing or malformed. Check your .env file!")

# === Constants ===
MODEL = "gpt-4o-mini"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

LINK_SYSTEM_PROMPT = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

BROCHURE_SYSTEM_PROMPT = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors, and recruits.
Respond in markdown. Include details of company culture, customers, and careers/jobs if available.
"""

# === Classes ===

class Website:
    def __init__(self, url: str):
        self.url = url
        self.title: str = ""
        self.text: str = ""
        self.links: List[str] = []
        self._fetch()

    def _fetch(self):
        response = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        self.title = soup.title.string if soup.title else "No title found"
        
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        raw_links = [a.get("href") for a in soup.find_all("a")]
        self.links = [link for link in raw_links if link and not link.startswith("mailto:")]

    def get_contents(self) -> str:
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n"

class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_json_response(self, model: str, system_prompt: str, user_prompt: str) -> Dict:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def get_markdown_response(self, model: str, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content

class BrochureBuilder:
    def __init__(self, openai_client: OpenAIClient):
        self.openai = openai_client

    def get_links(self, website: Website) -> List[Dict[str, str]]:
        user_prompt = (
            f"Here is the list of links on the website of {website.url} - "
            "please decide which of these are relevant web links for a brochure about the company. "
            "Do not include Terms of Service, Privacy, or email links.\n"
            "Links:\n" + "\n".join(website.links)
        )
        return self.openai.get_json_response(MODEL, LINK_SYSTEM_PROMPT, user_prompt).get("links", [])

    def collect_all_details(self, main_url: str) -> str:
        main_site = Website(main_url)
        result = f"Landing page:\n{main_site.get_contents()}"

        links = self.get_links(main_site)
        print("Found links:", links)

        for link in links:
            try:
                page = Website(link["url"])
                result += f"\n\n{link['type'].capitalize()}:\n{page.get_contents()}"
            except Exception as e:
                print(f"Error fetching {link['url']}: {e}")
        
        return result[:5000]  # Optional truncation

    def create_brochure(self, company_name: str, url: str):
        all_content = self.collect_all_details(url)
        user_prompt = (
            f"You are looking at a company called: {company_name}\n"
            f"Here are the contents of its landing page and other relevant pages:\n{all_content}"
        )
        brochure_md = self.openai.get_markdown_response(MODEL, BROCHURE_SYSTEM_PROMPT, user_prompt)
        display(Markdown(brochure_md))

# === Execution ===
if __name__ == "__main__":
    client = OpenAIClient(api_key)
    builder = BrochureBuilder(client)
    builder.create_brochure("itsolution.pl", "https://itsolution.pl")
