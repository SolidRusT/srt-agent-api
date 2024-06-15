import requests

API_BASE_URL = "http://127.0.0.1:8000"

def main():
    while True:
        user_input = input(">")
        if user_input == "exit":
            break
        elif user_input.startswith("fetch:"):
            url = user_input[len("fetch:"):].strip()
            response = requests.get(f"{API_BASE_URL}/fetch", params={"url": url})
            print(f"Fetched Data: {response.json()}")
        elif user_input.startswith("fetch_list:"):
            url = user_input[len("fetch_list:"):].strip()
            response = requests.get(f"{API_BASE_URL}/fetch_list", params={"url": url})
            print(f"Fetched Data List: {response.json()}")
        elif user_input.startswith("search:"):
            query = user_input[len("search:"):].strip()
            response = requests.get(f"{API_BASE_URL}/search", params={"query": query})
            print(f"Search Results: {response.json()}")
        elif user_input.startswith("wiki:"):
            title = user_input[len("wiki:"):].strip()
            response = requests.get(f"{API_BASE_URL}/wiki", params={"title": title})
            print(f"Summary: {response.json()}")
        else:
            response = requests.post(f"{API_BASE_URL}/chat", json={"message": user_input})
            print(f"Agent: {response.json()['response']}")

if __name__ == "__main__":
    main()
