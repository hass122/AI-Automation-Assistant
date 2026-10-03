import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_demo_jobs():
    """Fetch demo records from a public REST API."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    records = response.json()[:12]

    jobs = []
    for item in records:
        jobs.append({
            "id": item["id"],
            "title": item["title"].replace("-", " ").title(),
            "description": item["body"]
        })
    return jobs
