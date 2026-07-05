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
            response = requests.get(off_url)
            if response.status_code == 200:
                api_data = response.json()
                if api_data.get('status') == 1: 
                    product_info = api_data.get('product', {})
                    name = product_info.get('product_name', name)
                    brand = product_info.get('brands', brand)
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

@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_product(item_id):
    """UPDATE: Modify an existing product in the array."""
    data = request.json or {}
    for item in inventory:
        if item['id'] == item_id:
            item['name'] = data.get('name', item['name'])
            item['brand'] = data.get('brand', item['brand'])
            item['barcode'] = data.get('barcode', item['barcode'])
            return jsonify({"message": "Product updated", "product": item}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_product(item_id):
    """DELETE: Remove a product from the array."""
    global inventory
    inventory = [item for item in inventory if item['id'] != item_id]
    return jsonify({"message": "Product deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)