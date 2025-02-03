import requests
import os
import json
from bs4 import BeautifulSoup
from markdownify import markdownify
from dotenv import load_dotenv

load_dotenv()

def summarise_website(url):
    markdown_content = scrape_website_as_markdown(url)
    summary = summarise_markdown(markdown_content)
    return summary


def scrape_website_as_markdown(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid blocking
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        markdown_content = markdownify(str(soup), strip=['script', 'style'])  # Convert HTML to Markdown
        return markdown_content
    else:
        return f"Failed to retrieve content, status code: {response.status_code}"






def summarise_markdown(markdown_content):
    messages = [
        {
            "role" : "user",
            "content" : "You are a helpful assistant that summarises website markdown content."
        },
        {   
            "role": "user", 
            "content": markdown_content
        }
    ]
    response = requests.post('http://localhost:11434/api/chat', json={"model" : "llama3.2", "messages" : messages, "stream" : False}, headers={"Content-Type" : "application/json"})
    return response.json()['message']['content']
    




print(summarise_website("https://en.wikipedia.org/wiki/Pondicherry"))