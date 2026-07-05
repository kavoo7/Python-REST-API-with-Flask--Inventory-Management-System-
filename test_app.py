import unittest
import json
from app import app, inventory

class InventoryApiTestCase(unittest.TestCase):

    def setUp(self):
        """Reset the testing environment before each individual test."""
        self.app = app.test_client()
        self.app.testing = True
        inventory.clear()

    def test_create_and_get_inventory(self):
        """Test adding an item manually and immediately retrieving it."""
        self.app.post('/inventory', json={"name": "Apple", "brand": "FruitCo"})
        
        response = self.app.get('/inventory')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Apple")

    def test_delete_inventory(self):
        """Test deleting an item safely out of the array layout."""
        # Create an item and capture what ID was generated
        resp = self.app.post('/inventory', json={"name": "Banana"})
        created_data = json.loads(resp.data)
        item_id = created_data['product']['id']
        
        # Fire the delete target request
        delete_resp = self.app.delete(f'/inventory/{item_id}')
        self.assertEqual(delete_resp.status_code, 200)
        
        # Verify the array list is now empty
        get_resp = self.app.get('/inventory')
        self.assertEqual(len(json.loads(get_resp.data)), 0)

    def test_openfoodfacts_integration(self):
        """Test fetching an item barcode live (Nutella)."""
        response = self.app.post('/inventory', json={"barcode": "3017620422003"})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        
        # Combine string evaluations to catch variations in naming cases
        combined_text = f"{data['product']['brand']} {data['product']['name']}".lower()
        self.assertIn("nutella", combined_text)

if __name__ == '__main__':
    unittest.main()