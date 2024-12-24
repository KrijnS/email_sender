import requests

# Base URL for your API
BASE_URL = "https://example.com/api"

# Login endpoint and credentials
LOGIN_ENDPOINT = "/auth/login"
USERNAME = "your_username"
PASSWORD = "your_password"

# Subsequent endpoint
DATA_ENDPOINT = "/data"

def main():
    # Start a session
    session = requests.Session()

    # Login to the API
    login_response = session.post(
        f"{BASE_URL}{LOGIN_ENDPOINT}",
        json={"username": USERNAME, "password": PASSWORD}
    )

    if login_response.status_code == 200:
        print("Login successful!")
    else:
        print("Login failed:", login_response.text)
        return

    # Use the session to make authenticated requests
    data_response = session.get(f"{BASE_URL}{DATA_ENDPOINT}")

    if data_response.status_code == 200:
        print("Data fetched successfully:", data_response.json())
    else:
        print("Failed to fetch data:", data_response.text)

if __name__ == "__main__":
    main()
