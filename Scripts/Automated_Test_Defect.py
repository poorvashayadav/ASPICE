import os
import requests
import unittest
from unittest.mock import MagicMock

# Configuration
TRACKER_ID = 3606  # Tracker ID for "Defect-Bug Reports"
API_URL = f"http://20.235.210.85:8080/cb/api/v3/trackers/{TRACKER_ID}/items"
AUTH = (os.getenv('cb_user'), os.getenv('cb_password'))
HEADERS = {
    "Content-Type": "application/json"
}

# Mock classes to simulate behavior
class MockCarla:
    class Client:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.world = MockWorld()

        def get_world(self):
            return self.world

class MockWorld:
    def __init__(self):
        self.actor = MagicMock()

# Function to log defect
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

# Test case
class TestCarlaSimulated(unittest.TestCase):

    def test_no_collision(self):
        client = MockCarla.Client('localhost', 2000)
        client.get_world().actor.check_collision = MagicMock(return_value=False)
        self.assertFalse(client.get_world().actor.check_collision())

    def test_collision(self):
        client = MockCarla.Client('localhost', 2000)
        client.get_world().actor.check_collision = MagicMock(return_value=True)

        try:
            self.assertFalse(client.get_world().actor.check_collision())
        except AssertionError as e:
            log_defect("test_collision", str(e))

    def test_actor_exists(self):
        client = MockCarla.Client('localhost', 2000)
        client.get_world().actor.exists = MagicMock(return_value=False)

        try:
            self.assertTrue(client.get_world().actor.exists())
        except AssertionError as e:
            log_defect("test_actor_exists", str(e))

if __name__ == '__main__':
    unittest.main()
