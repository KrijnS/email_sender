# USAGE:
# echo "<cookies>" | docker secret create login_cookies -

# docker build -t s-run_status .

#docker service create --name s-run_status_checker --secret login_cookies s-run_status


# Note, the cookies should be generated in Postman using the login endpoint and then copied to the secret.
# This endpoint is the POST http://localhost:81/Account/LoginUser endpoint. And will automatically generate 2 cookies after POST.
# These can be copied as one value in the secret from the body. It's inconvenient but a workaround, since code only gives the first cookie.

import requests
import time
import os

# Base URL for your API
BASE_URL = "http://host.docker.internal:81"  # Use host.docker.internal if running the API on the host machine

# Path to the secret
COOKIE_SECRET_PATH = "/run/secrets/login_cookies"

# Function to read the secret
def get_cookie_secret():
    try:
        with open(COOKIE_SECRET_PATH, "r") as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        print(f"Secret file {COOKIE_SECRET_PATH} not found. Exiting.")
        return None

# New endpoint to fetch execution IDs in error
EXECUTION_IDS_ENDPOINT = "/api/api/GetExecutionIdsInError"

def main():
    # Read the cookie secret
    cookie_secret = get_cookie_secret()
    if not cookie_secret:
        print("Cookie secret is missing. Exiting.")
        return

    # Start a session to persist cookies
    session = requests.Session()
    
    headers = {
        'Cookie': cookie_secret
    }

    seen_process_execution_ids = set()

    while True:
        # Make the GET request to fetch execution IDs in error
        data_response = session.get(f"{BASE_URL}{EXECUTION_IDS_ENDPOINT}", headers=headers)
        
        # Check the response status and handle it
        print("Status Code for GetExecutionIdsInError:", data_response.status_code)
        
        if data_response.status_code == 200:
            try:
                # Attempt to parse the response as JSON
                execution_ids = data_response.json()
                if execution_ids:
                    for error in execution_ids:
                        process_execution_id = error['processExecutionId']
                        if process_execution_id not in seen_process_execution_ids:
                            seen_process_execution_ids.add(process_execution_id)
                            print(f"Error ID: {error['id']}, Process ID: {process_execution_id}, Status: {error['status']}, Name: {error['name']}")
                else:
                    print("No new error IDs found")
            except ValueError:
                print("Response is not in JSON format.")
        else:
            print("Failed to fetch execution IDs.")
        
        # Wait for 10 seconds before making the next request
        time.sleep(10)

if __name__ == "__main__":
    main()
