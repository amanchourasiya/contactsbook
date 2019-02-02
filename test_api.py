import requests,unittest
from requests.auth import HTTPBasicAuth
import json

class TestContactsApi(unittest.TestCase):
    def test_get_contacts_by_email(self):
        expected_result = {
            'result': [
                {'name':'aman',
                 'email':'amanchourasia6@gmail.com',
                 'mobile':'8982742221',
                 'city':'Bangalore'
                 }]
        }
        url = 'http://127.0.0.1:5000/contacts/api/v1.0/email/amanchourasia6@gmail.com'
        actual_result = requests.get(url, auth=('aman','aman')).json()
        self.assertEqual(expected_result,actual_result)

    def test_insert_user(self):
        expected_result = {
            'result':'success'
        }
        data = {
            'name':  'user1',
            'email': 'user11@gmail.com',
            'mobile': '12345',
            'city': 'Bangalore'
        }
        headers = {'Content-Type': 'application/json'}
        url = 'http://127.0.0.1:5000/contacts/api/v1.0'
        print(data)
        actual_result = requests.post(url, json =data, headers=headers, auth=('aman','aman')).json()
        self.assertEqual(expected_result, actual_result)

    def test_delete_user_by_name(self):
        expected_result = {'result':'success'}
        url = 'http://127.0.0.1:5000/contacts/api/v1.0/name/user1'
        actual_result = requests.delete(url, auth=('aman','aman')).json()
        self.assertEqual(expected_result,actual_result)

    def test_update_user(self):
        expected_result = {'result':'success'}
        url = 'http://127.0.0.1:5000/contacts/api/v1.0/email/user1@gmail.com'
        data = {
            'name':'user1',
            'mobile':'11111',
            'city':'mumbai'
        }
        headers = {'Content-Type':'application/json'}
        actual_result = requests.put(url, json=data, headers=headers, auth=('aman','aman')).json()
        self.assertEqual(expected_result, actual_result)

    def test_authorization(self):
        expected_result = {'error':'unauthorized'}
        url = 'http://127.0.0.1:5000/contacts/api/v1.0/email/user1@gmail.com'
        actual_result = requests.get(url).json()
        self.assertEqual(expected_result,actual_result)

if __name__ == '__main__':
    unittest.main()