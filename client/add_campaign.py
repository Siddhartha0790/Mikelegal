import requests
import sys
from datetime import datetime, timezone

BASE_URL = "http://localhost:8000/api"

def add_campaign(subject, preview_text, article_url, html_content, plain_text_content, username="admin", password="password"):
    """
    add campaign
    """
    url = f"{BASE_URL}/campaigns/"
    
    # We set published_date to right now so it sends today
    now_iso = datetime.now(timezone.utc).isoformat()
    
    payload = {
        "subject": subject,
        "preview_text": preview_text,
        "article_url": article_url,
        "html_content": html_content,
        "plain_text_content": plain_text_content,
        "published_date": now_iso
    }
    
    print(f"POST {url} with campaign: '{subject}'")
    
    try:
        response = requests.post(url, json=payload, auth=(username, password))
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error")

if __name__ == "__main__":
    # default campaign
    subject = "Welcome to Mike Legal's New Campaign Feature"
    preview_text = "Check out our latest update."
    article_url = "https://example.com/mike-legal-update"
    html_content = "<html><body><h1>Hello!</h1><p>This is a new campaign.</p></body></html>"
    plain_text_content = "Hello! This is a new campaign."
    
    # get credentials from terminal
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "password"
    
    add_campaign(
        subject, 
        preview_text, 
        article_url, 
        html_content, 
        plain_text_content, 
        username, 
        password
    )
