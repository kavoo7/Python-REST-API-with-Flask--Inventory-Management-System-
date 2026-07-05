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
        # Create
        self.app.post('/inventory', json={"name": "Apple", "brand": "FruitCo"})
        
        # Read
        response = self.app.get('/inventory')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Apple")

    def test_delete_inventory(self):
        """Test deleting an item safely out of the array layout."""
        self.app.post('/inventory', json={"name": "Banana"})
        
        # Assume it gets sequence ID 1 because the array resets clean
        delete_resp = self.app.delete('/inventory/1')
        self.assertEqual(delete_resp.status_code, 200)
        
        get_resp = self.app.get('/inventory')
        self.assertEqual(len(json.loads(get_resp.data)), 0)

    def test_openfoodfacts_integration(self):
        """Test fetching an item barcode live (Nutella)."""
        response = self.app.post('/inventory', json={"barcode": "3017620422003"})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("Nutella", data['product']['brand'] or data['product']['name'])

if __name__ == '__main__':
    unittest.main()