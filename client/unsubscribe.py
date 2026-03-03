import requests
import sys

BASE_URL = "http://localhost:8000/api"

def unsubscribe(email):
    """
    Deactivates a subscriber based on their email.
    """
    url = f"{BASE_URL}/unsubscribe/"
    payload = {
        "email": email
    }
    
    print(f"POST {url} with data: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it is running on http://localhost:8000")

if __name__ == "__main__":
    # You can pass the email to unsubscribe from the terminal or it defaults to this
    email = sys.argv[1] if len(sys.argv) > 1 else "john.doe@example.com"
    
    unsubscribe(email)
