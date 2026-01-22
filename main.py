import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

def main_thread():
    server_url = os.getenv("GITHUB_SERVER_URL")
    repo = os.getenv("GITHUB_REPOSITORY")
    run_id = os.getenv("GITHUB_RUN_ID")
    action_run_link = f"{server_url}/{repo}/actions/runs/{run_id}"
    
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    content = {
        "timestamp": timestamp,
        "name": "Blaze Zhenli",
        "email": "blazezhenli@gmail.com",
        "resume_link": "https://drive.google.com/file/d/1bnbFZuMkc0bLBcdR6X7OyptLrv5IxLRQ/view?usp=drive_link",
        "repository_link": f"{server_url}/{repo}",
        "action_run_link": action_run_link
    }
    
    payload_json = json.dumps(content, sort_keys=True, separators=(',', ':'))
    payload_bytes = payload_json.encode('utf-8')
    
    signing_secret = os.getenv("SIGNING_SECRET", "default-for-local-testing")
    
    signature = hmac.new(
        signing_secret.encode('utf-8'), 
        payload_bytes, 
        hashlib.sha256
    ).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}"
    }
    
    response = requests.post(
        "https://b12.io/apply/submission", 
        data=payload_bytes, 
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main_thread()