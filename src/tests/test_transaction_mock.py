import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from database.connMongoDB import db
from src.controller.transactionController import app_router

client = TestClient(app_router)

class TestTransaction(unittest.TestCase):
    
    @patch('db')
    def test_authorize_approved(self, mock_db):
        mock_db["account"].find_one.return_value = {
            "accountId": "1234",
            "balances": {
                "FOOD": 200.0,
                "MEAL": 100.0,
                "CASH": 300.0
            }
        }
        
        transaction = {
            "account": "1234",
            "totalAmount": 50.0,
            "mcc": "5411",
            "merchant": "TESTE"
        }
        response = client.post("/authorize", json=transaction)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"code": "00"})

    @patch('app.db')
    def test_authorize_insufficient_funds(self, mock_db):
        mock_db["account"].find_one.return_value = {
            "accountId": "1234",
            "balances": {
                "FOOD": 200.0,
                "MEAL": 100.0,
                "CASH": 300.0
            }
        }
        
        transaction = {
            "account": "1234",
            "totalAmount": 150.0,
            "mcc": "5811",
            "merchant": "PADARIA DO ZE               SAO PAULO BR"
        }
        response = client.post("/authorize", json=transaction)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"code": "51"})

    @patch('app.db')
    def test_authorize_fallback_to_cash(self, mock_db):
        mock_db["account"].find_one.return_value = {
            "accountId": "1234",
            "balances": {
                "FOOD": 50.0,
                "MEAL": 20.0,
                "CASH": 300.0
            }
        }
        
        transaction = {
            "account": "1234",
            "totalAmount": 120.0,
            "mcc": "5411",
            "merchant": "TESTE"
        }
        response = client.post("/authorize", json=transaction)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"code": "00"})
        
        updated_account = mock_db["account"].find_one.return_value
        self.assertEqual(updated_account["balances"]["CASH"], 180.0)

    @patch('app.db')
    def test_authorize_merchant_override(self, mock_db):
        mock_db["account"].find_one.return_value = {
            "accountId": "1234",
            "balances": {
                "FOOD": 200.0,
                "MEAL": 100.0,
                "CASH": 300.0
            }
        }
        
        transaction = {
            "account": "1234",
            "totalAmount": 80.0,
            "mcc": "0000",
            "merchant": "UBER EATS   SAO PAULO BR"
        }
        response = client.post("/authorize", json=transaction)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"code": "00"})
        
        updated_account = mock_db["account"].find_one.return_value
        self.assertEqual(updated_account["balances"]["MEAL"], 20.0)

if __name__ == "__main__":
    unittest.main()
