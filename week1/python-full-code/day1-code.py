import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
from IPython.display import Markdown, display
from pathlib import Path
from dotenv import load_dotenv  # można usunąć, jeśli nie używasz w terminalu

# ==============================
# CONFIG & ENV SETUP
# ==============================

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Prosta walidacja klucza API
def validate_api_key(key: str) -> bool:
    if not key:
        print("No API key found. Check your .env file.")
        return False
    if not key.startswith("sk-proj-"):
        print("API key found, but it doesn't start with 'sk-proj-'")
        return False
    if key.strip() != key:
        print("API key contains leading/trailing spaces.")
        return False
    print("API key looks valid.")
    return True

# ==============================
# SCRAPER CLASS
# ==============================

class Website:
    def __init__(self, url: str):
        """
        Create Website object using BeautifulSoup to extract title and visible text.
        """
        self.url = url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/117.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.title = soup.title.string if soup.title else "No title found"

        for tag in soup.body(["script", "style", "img", "input"]):
            tag.decompose()

        self.text = soup.body.get_text(separator="\n", strip=True)

# ==============================
# PROMPTS
# ==============================

system_prompt = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that might be navigation related. "
    "Respond in markdown."
)

def user_prompt_for(website: Website) -> str:
    return (
        f"You are looking at a website titled: {website.title}\n\n"
        "The contents of this website is as follows. Please provide a short summary in markdown. "
        "If it includes news or announcements, summarize them as well:\n\n"
        f"{website.text}"
    )

def messages_for(website: Website) -> list:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# ==============================
# SUMMARY FUNCTION
# ==============================

def summarize(url: str) -> str:
    website = Website(url)
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(website)
    )

    return response.choices[0].message.content

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    if validate_api_key(api_key):
        url = "https://wykop.pl"
        print(f"Summarizing website: {url}\n")
        try:
            summary = summarize(url)
            print(summary)
        except Exception as e:
            print(f"Error during summarization: {e}")
