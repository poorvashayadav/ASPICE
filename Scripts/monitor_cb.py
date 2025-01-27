import requests
import pandas as pd

def check_codebeamer_health(url):
    try:
        # Send a GET request to the main URL
        response = requests.get(url)
        
        # Prepare table data
        if response.status_code == 200:
            health_data = {
                "Attribute": ["URL", "Status Code", "Status"],
                "Value": [
                    url,
                    response.status_code,
                    "Reachable"
                ],
            }
        else:
            health_data = {
                "Attribute": ["URL", "Status Code", "Status"],
                "Value": [
                    url,
                    response.status_code,
                    "Unreachable"
                ],
            }
        
        # Create a DataFrame and display it
        df = pd.DataFrame(health_data)
        print("\nCodeBeamer Health Check:")
        print(df.to_string(index=False))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace with your CodeBeamer instance details
    CODEBEAMER_URL = "http://20.235.210.85:8080/cb"

    print("\nChecking CodeBeamer instance...")
    check_codebeamer_health(CODEBEAMER_URL)
