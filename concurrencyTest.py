import requests
import concurrent.futures
import uuid
import time

def send_request(url, headers, data):
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        end_time = time.time()
        return response.content.decode('utf-8'), end_time - start_time
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}, 0

def main():
    url = 'http://127.0.0.1:5000/sql/company/store'
    headers = {
        'X-Encrypted-Key': 'gAkhJbEBXzR5CVj2rngd9S1kL+FFAGeAGvkmbIx1CUpvshOXceq80P58/qAKAajz',
        'Content-Type': 'application/json'
    }

    # Number of concurrent requests to send
    num_requests = 100000

    total_time = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Send concurrent requests
        futures = [executor.submit(send_request, url, headers, generate_data()) for _ in range(num_requests)]

        # Wait for all requests to complete
        for future in concurrent.futures.as_completed(futures):
            result, request_time = future.result()
            # print(result)
            total_time += request_time

    print(f"Total time taken: {total_time} seconds")
    print(f"Average time per request: {total_time / num_requests} seconds")

def generate_data():
    # Generate a random ID
    random_id = str(uuid.uuid4())
    data = {
        "ID": random_id,
        "DATA": {
            "NAME": "Test"
        }
    }
    return data

if __name__ == "__main__":
    main()
