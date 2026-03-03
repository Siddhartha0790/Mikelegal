import requests
import sys

BASE_URL = "http://localhost:8000/api"

def add_subscriber(email, first_name):
    """
    Adds a new subscriber to the database.
    """
    url = f"{BASE_URL}/subscribers/"
    payload = {
        "email": email,
        "first_name": first_name
    }
    
    print(f"POST {url} with data: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it is running on http://localhost:8000")

if __name__ == "__main__":
    # You can pass arguments from the terminal or it will use these defaults
    email = sys.argv[1] if len(sys.argv) > 1 else "b123130@iiit-bh.ac.in"
    first_name = sys.argv[2] if len(sys.argv) > 2 else "siddharth"
    
    add_subscriber(email, first_name)
