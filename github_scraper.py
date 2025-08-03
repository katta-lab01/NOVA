# scraper/github_scraper.py

import requests
from typing import List, Optional
import logging

class GitHubScraper:
    """
    Scrapes issues from a public GitHub repository using GitHub REST API.
    Can filter issues by a keyword in title or body.
    """

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def scrape(self, repo_url: str, query: Optional[str] = None, max_issues: int = 10) -> List[str]:
        try:
            parts = repo_url.rstrip("/").split("/")[-2:]
            if len(parts) != 2:
                raise ValueError("Invalid GitHub repo URL")

            owner, repo = parts
            api_url = f"https://api.github.com/repos/{owner}/{repo}/issues?per_page={max_issues}"
            response = requests.get(api_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            issues = response.json()

            results = []
            for issue in issues:
                if 'pull_request' in issue:
                    continue
                title = issue.get('title', '').strip()
                body = issue.get('body', '').strip()
                content = f"{title}\n{body}".lower()
                if query:
                    if query.lower() in content:
                        results.append(f"Issue: {title}\n{body}")
                else:
                    results.append(f"Issue: {title}\n{body}")

            return results

        except Exception as e:
            logging.error(f"[GitHubScraper] Error scraping repo {repo_url}: {e}")
            return []
