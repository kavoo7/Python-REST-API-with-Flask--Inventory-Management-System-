from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Simulated data storage (Array/List)
inventory = []
next_id = 1

@app.route('/inventory', methods=['GET'])
def get_inventory():
    """READ: Fetch all items in the inventory."""
    return jsonify(inventory), 200

@app.route('/inventory', methods=['POST'])
def add_product():
    """CREATE: Add a product. Fetches from OpenFoodFacts if barcode is provided."""
    global next_id
    data = request.json or {}
    barcode = data.get('barcode')
    
    name = data.get('name', 'Unknown Product')
    brand = data.get('brand', 'Unknown Brand')

    # External API Integration
    if barcode:
        off_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        try:
            # Added a standard User-Agent header which OpenFoodFacts requires to prevent throttling
            headers = {'User-Agent': 'EcommerceAdminPortal - Python - Version 1.0'}
            response = requests.get(off_url, headers=headers, timeout=5)
            if response.status_code == 200:
                api_data = response.json()
                if api_data.get('status') == 1 or api_data.get('status_verbose') == "product found": 
                    product_info = api_data.get('product', {})
                    name = product_info.get('product_name', name)
                    # Fallback sequences to look up brands
                    brand = product_info.get('brands', product_info.get('brand_owner', brand))
        except Exception as e:
            print(f"Error connecting to OpenFoodFacts: {e}")

    new_item = {
        "id": next_id,
        "name": name,
        "barcode": barcode,
        "brand": brand
    }
    inventory.append(new_item)
    next_id += 1
    
    return jsonify({"message": "Product created", "product": new_item}), 201

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_product(item_id):
    """DELETE: Remove a product from the array safely."""
    global inventory
    target_item = None
    for item in inventory:
        if item['id'] == item_id:
            target_item = item
            break
            
    if target_item:
        inventory.remove(target_item)
        return jsonify({"message": "Product deleted"}), 200
        
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)