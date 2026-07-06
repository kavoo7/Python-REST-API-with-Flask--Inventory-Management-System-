# Inventory Management System

A simple Flask-based inventory management API with an accompanying command-line client. The project lets you create, view, update, and delete inventory items, and it can enrich products with data from OpenFoodFacts using a barcode.

## Features

- Manage inventory through a REST API
- Add products manually or by barcode lookup
- Update product price and stock
- Delete inventory items
- Interact with the API through a Python CLI
- Includes automated tests for the main API flows

## Tech Stack

- Python 3
- Flask
- requests
- unittest

## Project Structure

- app.py: Flask application and REST endpoints
- cli.py: Command-line interface for interacting with the API
- test_app.py: Unit tests for the API
- requirements.txt: Python dependencies

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the Flask server:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Get all inventory items

```bash
curl http://127.0.0.1:5000/inventory
```

### Add a product

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name":"Apple","brand":"FruitCo","price":1.25,"stock":50}'
```

### Add a product using a barcode

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"barcode":"3017620422003","price":2.99,"stock":20}'
```

### Update a product's price or stock

```bash
curl -X PUT http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"price":2.5}'
```

### Delete a product

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

## CLI Usage

Run the CLI with:

```bash
python cli.py
```

Example commands:

```bash
python cli.py list
python cli.py add "Apple" 1.25 50
python cli.py fetch 3017620422003 2.99 20
python cli.py update 1 price 2.50
python cli.py delete 1
python cli.py find 3017620422003
```

## Testing

Run the test suite:

```bash
python -m unittest -v
```

## Notes

- Inventory data is stored in memory while the server is running.
- If the server is restarted, the inventory list resets.
- Barcode lookup uses the OpenFoodFacts API and falls back gracefully if the request fails.
