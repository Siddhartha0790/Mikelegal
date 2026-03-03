import requests

BASE_URL = "http://localhost:8000/api"

def get_subscribers():
    """
    fetch subscribers
    """
    url = f"{BASE_URL}/subscribers/"
    print(f"GET {url}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        # parse json
        if response.ok:
            data = response.json()
            print("Response Data:")
            for subscriber in data.get('results', data): # pg
                print(f" - {subscriber['first_name']} ({subscriber['email']})")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it is running on http://localhost:8000")

if __name__ == "__main__":
    get_subscribers()
