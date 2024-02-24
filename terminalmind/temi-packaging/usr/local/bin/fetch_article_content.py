#!/usr/bin/env python3
"""Fetch the article content based on user's url.
"""
import sys
import requests
from bs4 import BeautifulSoup


def fetch_article_content(url):
    """Fetch article content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("article")
        paragraphs = article.find_all("p")
        return " ".join([para.get_text() for para in paragraphs])
    except Exception as e:
        return f"Error: {e}"


def main():
    """Fetch the article content."""
    if len(sys.argv) != 2:
        print("Usage: fetch_article_content.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    content = fetch_article_content(url)
    print(content)


if __name__ == "__main__":
    main()
