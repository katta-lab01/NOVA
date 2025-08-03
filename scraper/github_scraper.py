# scraper/github_scraper.py

import requests
import random
import time
from typing import List, Optional
import logging

class GitHubScraper:
    """
    Scrapes issues from a public GitHub repository using GitHub REST API.
    Can filter issues by a keyword in title or body.
    """

    USER_AGENTS = [
        "Mozilla/5.0 ... Chrome/120.0.0.0 ...",
        "Mozilla/5.0 ... Firefox/115.0 ...",
        # Add more user agents
    ]

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def get_random_user_agent(self):
        return random.choice(self.USER_AGENTS)

    def scrape(self, repo_url: str, query: Optional[str] = None, max_issues: int = 10, retries: int = 3) -> List[str]:
        try:
            parts = repo_url.rstrip("/").split("/")[-2:]
            if len(parts) != 2:
                raise ValueError("Invalid GitHub repo URL")

            owner, repo = parts
            api_url = f"https://api.github.com/repos/{owner}/{repo}/issues?per_page={max_issues}"

            for attempt in range(retries):
                headers = self.headers.copy()
                headers["User-Agent"] = self.get_random_user_agent()
                try:
                    response = requests.get(api_url, headers=headers, timeout=10)
                    if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
                        reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                        wait_seconds = max(reset_time - int(time.time()), 5)
                        logging.warning(f"Rate limit reached. Waiting {wait_seconds} seconds.")
                        time.sleep(wait_seconds)
                        continue
                    response.raise_for_status()
                    issues = response.json()
                    break
                except Exception as e:
                    logging.warning(f"Attempt {attempt+1} failed: {e}")
                    time.sleep(random.uniform(2, 5))
            else:
                logging.error(f"[GitHubScraper] All attempts failed for repo {repo_url}")
                return []

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
