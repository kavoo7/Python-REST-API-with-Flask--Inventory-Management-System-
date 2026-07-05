import sys
import requests

BASE_URL = "http://127.0.0.1:5000/inventory"

def print_help():
    print("""
=========================================
      E-COMMERCE ADMIN PORTAL CLI        
=========================================
Commands:
  list                                    - View inventory details
  add <name> <price> <stock>              - Add new inventory item manually
  fetch <barcode> <price> <stock>         - Add via OpenFoodFacts lookup
  update <id> <price/stock> <new_value>   - Update item prices or stock levels
  delete <id>                             - Delete products
  find <barcode>                          - Find item on external API directly
""")

def handle_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        if response.status_code in [200, 201]:
            print(f"\n[SUCCESS]\n", response.json())
        else:
            print(f"\n[API ERROR {response.status_code}]\n", response.text)
    except requests.exceptions.ConnectionError:
        print("\n[CRITICAL ERROR] Could not connect to backend server. Is app.py running?")

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print_help()
        sys.exit(1)
        
    command = args[0].lower()
    
    if command == "list":
        handle_request("GET", BASE_URL)
        
    elif command == "add":
        if len(args) < 4:
            print("[Input Error] Missing arguments. Usage: add <name> <price> <stock>")
        else:
            try:
                # Basic input validation validation
                payload = {"name": args[1], "price": float(args[2]), "stock": int(args[3])}
                handle_request("POST", BASE_URL, json=payload)
            except ValueError:
                print("[Input Error] Price must be a decimal number, and Stock must be an integer.")
                
    elif command == "fetch":
        if len(args) < 4:
            print("[Input Error] Missing arguments. Usage: fetch <barcode> <price> <stock>")
        else:
            try:
                payload = {"barcode": args[1], "price": float(args[2]), "stock": int(args[3])}
                handle_request("POST", BASE_URL, json=payload)
            except ValueError:
                print("[Input Error] Price must be a decimal number, and Stock must be an integer.")

    elif command == "update":
        if len(args) < 4:
            print("[Input Error] Missing arguments. Usage: update <id> <price/stock> <new_value>")
        else:
            item_id = args[1]
            field = args[2].lower()
            val = args[3]
            if field not in ['price', 'stock']:
                print("[Input Error] Field choice must be either 'price' or 'stock'.")
            else:
                try:
                    payload = {field: float(val) if field == 'price' else int(val)}
                    handle_request("PUT", f"{BASE_URL}/{item_id}", json=payload)
                except ValueError:
                    print(f"[Input Error] Invalid value assignment for {field}.")

    elif command == "delete" and len(args) == 2:
        handle_request("DELETE", f"{BASE_URL}/{args[1]}")
        
    elif command == "find" and len(args) == 2:
        # Find item directly on the external web service without editing local store items
        print(f"Searching OpenFoodFacts Database for barcode: {args[1]}...")
        try:
            res = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{args[1]}.json")
            if res.status_code == 200 and res.json().get('status') == 1:
                p = res.json()['product']
                print(f"\n[FOUND] Brand: {p.get('brands','N/A')} | Name: {p.get('product_name','N/A')}")
            else:
                print("\n[API Error] Product barcode not found in the global library database.")
        except Exception as e:
            print(f"[API Failure] Failed to reach global servers: {e}")
            
    else:
        print("\nInvalid Command Combination entered.")
        print_help()