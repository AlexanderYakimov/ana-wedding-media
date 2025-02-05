import unittest
from app import create_app

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestConfig")
        self.client = self.app.test_client()
    
    def test_homepage(self):
        """
        Tests the main page content and status code.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Галерея", response.data.decode("utf-8"))
    
    def test_api(self):
        """
        Test the photo api.
        """
        response = self.client.get("/api/photos?limit=2&offset=0")
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data["files"], ["1.jpg", "2.jpg"])
    
    def test_404_page(self):
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)
        self.assertIn(f"404", response.data.decode("utf-8"))
    

if __name__ == "__main__":
    unittest.main()
