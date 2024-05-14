import requests
import json

def run(body):
    try:
        # Assuming body is a dictionary or can be converted to a dictionary
        data = json.loads(body) if isinstance(body, str) else body
        
        url = "https://1291-45-112-55-42.ngrok-free.app/beneficiary/on_fund_transfer_transaction_status_changed"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Data forwarded successfully!")
            return "ok"
        else:
            print("Failed to forward data:", response.text)
            return "error"
    except Exception as e:
        return "Error : "+str(e)