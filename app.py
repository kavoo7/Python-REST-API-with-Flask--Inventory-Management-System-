from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = []
next_id = 1

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory', methods=['POST'])
def add_product():
    global next_id
    data = request.json or {}
    barcode = data.get('barcode')
    
    # Capture new rubric fields: price and stock
    name = data.get('name', 'Unknown Product')
    brand = data.get('brand', 'Unknown Brand')
    price = data.get('price', 0.0)
    stock = data.get('stock', 0)

    if barcode:
        off_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        try:
            headers = {'User-Agent': 'EcommerceAdminPortal - Python - Version 1.0'}
            response = requests.get(off_url, headers=headers, timeout=5)
            if response.status_code == 200:
                api_data = response.json()
                if api_data.get('status') == 1: 
                    product_info = api_data.get('product', {})
                    name = product_info.get('product_name', name)
                    brand = product_info.get('brands', brand)
        except Exception as e:
            print(f"External API Failure: {e}")

    new_item = {
        "id": next_id,
        "name": name,
        "barcode": barcode,
        "brand": brand,
        "price": float(price),
        "stock": int(stock)
    }
    inventory.append(new_item)
    next_id += 1
    
    return jsonify({"message": "Product created", "product": new_item}), 201

@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_product(item_id):
    """UPDATE: Handles modifying item prices or stock levels explicitly."""
    data = request.json or {}
    for item in inventory:
        if item['id'] == item_id:
            if 'price' in data:
                item['price'] = float(data['price'])
            if 'stock' in data:
                item['stock'] = int(data['stock'])
            return jsonify({"message": "Product updated successfully", "product": item}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_product(item_id):
    global inventory
    for item in inventory:
        if item['id'] == item_id:
            inventory.remove(item)
            return jsonify({"message": "Product deleted safely"}), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)