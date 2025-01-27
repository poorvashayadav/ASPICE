import os
import requests

TRACKER_ID = 186754  
API_URL = f"http://20.235.210.85:8080/cb/api/v3/trackers/{TRACKER_ID}/items"
AUTH = (os.getenv('cb_user'), os.getenv('cb_password'))
HEADERS = {
    "Content-Type": "application/json"
}

def log_defect(failed_test_name, failure_reason):
    payload = {
        "name": f"Test-Defect: {failed_test_name}",
        "descriptionFormat": "Wiki",
        "createdBy": {
            "id": 1,
            "name": "admin",
            "type": "UserReference",
            "email": "p.sudhir.kumar@accenture.com"
        },
        "priority": {
            "id": 3,
            "name": "Normal",
            "type": "ChoiceOptionReference"
        },
        "status": {
            "id": 1,
            "name": "New",
            "type": "ChoiceOptionReference"
        },
        "customFields": [
            {
                "fieldId": 10000,
                "name": "Failure Reason",
                "value": failure_reason,
                "type": "TextFieldValue"
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=payload, auth=AUTH, headers=HEADERS)
        if response.status_code == 201:
            print(f"Defect logged successfully for {failed_test_name}!")
        else:
            print(f"Failed to log defect for {failed_test_name}. Status: {response.status_code}")
            print("Response:", response.text)
    except requests.RequestException as e:
        print(f"Error during defect logging for {failed_test_name}:", e)
