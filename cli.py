import sys
import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

def print_help():
    print("""
Available Commands:
  list                 - View all products
  add <name>           - Add a product manually
  fetch <barcode>      - Fetch and add via OpenFoodFacts
  delete <id>          - Delete a product by its ID
    """)

def handle_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        if response.status_code in [200, 201]:
            print(f"\n[Success] {response.json()}")
        else:
            print(f"\n[Error {response.status_code}] {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nError: Cannot connect. Is app.py running?")

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print_help()
        sys.exit(1)
        
    command = args[0].lower()
    
    if command == "list":
        handle_request("GET", BASE_URL)
        
    elif command == "add" and len(args) > 1:
        payload = {"name": " ".join(args[1:])}
        handle_request("POST", BASE_URL, json=payload)
        
    elif command == "fetch" and len(args) == 2:
        payload = {"barcode": args[1]}
        handle_request("POST", BASE_URL, json=payload)

    elif command == "delete" and len(args) == 2:
        item_id = args[1]
        handle_request("DELETE", f"{BASE_URL}/{item_id}")
        
    else:
        print("Invalid command.")
        print_help()