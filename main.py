# imports
import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import google.generativeai as genai

# Load environment variables from a .env file and configure the API
load_dotenv()
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    print(f"Google API Key configured successfully, starting with: {api_key[:8]}...")
except Exception as e:
    print(f"Error configuring Google API: {e}")
    # Exit if the API key is not configured, as the script cannot run without it.
    exit()

# Some websites need you to use proper headers when fetching them to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

class Website:
    """
    A utility class to represent a scraped Website.
    It now handles request errors and resolves relative links to absolute URLs.
    """
    def __init__(self, url: str):
        self.url = url
        self.title = "No title found"
        self.text = ""
        self.links = []

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            self.title = soup.title.string if soup.title else "No title found"

            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input", "nav", "footer"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)

            for link_tag in soup.find_all('a', href=True):
                href = link_tag.get('href')
                absolute_link = urljoin(self.url, href)
                if urlparse(absolute_link).scheme in ["http", "https"]:
                    self.links.append(absolute_link)
            
            self.links = list(dict.fromkeys(self.links)) # Remove duplicates

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {self.url}: {e}")

    def get_contents(self) -> str:
        """Returns a string representation of the webpage's content."""
        return f"Webpage Title:\n{self.title}\n\nWebpage Contents:\n{self.text}\n"

# The system prompt defines the AI's role and the required JSON output format.
link_system_prompt = """
You are a helpful assistant that analyzes links from a company's website.
Your task is to identify links that would be most relevant for a company brochure, such as 'About Us', 'Company History', 'Careers', or 'Jobs' pages.

You MUST respond in a valid JSON format, as shown in this example:
{
  "links": [
    {"type": "about page", "url": "https://full.url/goes/here/about"},
    {"type": "careers page", "url": "https://another.full.url/careers"}
  ]
}
"""

def get_links_user_prompt(website: Website) -> str:
    """Creates the user prompt with the list of links for the AI model."""
    user_prompt = (
        f"Here is the list of links from the website {website.url}. "
        "Please identify the most relevant links for a company brochure. "
        "Respond with the full URL in the specified JSON format. "
        "Do not include links for 'Terms of Service', 'Privacy Policy', social media, or email addresses.\n\n"
        "Links:\n"
    )
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(url: str) -> dict:
    """
    Fetches a URL, scrapes its links, and uses the Gemini model to find relevant ones.
    """
    print(f"\nScraping website: {url}...")
    website = Website(url)

    if not website.links:
        print("No links found or failed to scrape the website.")
        return {"links": []}

    print(f"Found {len(website.links)} unique links. Analyzing with Gemini...")

    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=link_system_prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    user_prompt = get_links_user_prompt(website)
    
    try:
        response = model.generate_content(user_prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"An error occurred during Gemini API call: {e}")
        return {"links": []}







    



  
