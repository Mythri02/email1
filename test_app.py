import unittest
import json
from app import app

class TestPhishingDetection(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict(self):
        # Test valid prediction
        response = self.app.post('/predict', 
                                 data=json.dumps({"text": "Click here to claim your prize"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.json)

        # Test no text provided
        response = self.app.post('/predict', 
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_home(self):
        # Test root endpoint
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the Phishing Email Detection App', response.data.decode())

if __name__ == '__main__':
    unittest.main()
