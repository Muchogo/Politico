
import unittest
from flask import json
from ... import create_app
from .basetest import BaseTestCase
app = create_app()


class PartiesTest(BaseTestCase):
 
    def test_create_new_parties(self):
        result = self.app.post('/api/v1/parties', data=self.new_parties_data)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "New party created")

    def test_get_all_parties(self):
        result = self.app.get('/api/v1/parties')
        self.assertEqual(result.status_code, 200)

    def test_create_new_parties_user_doesnt_exist(self):
        result = self.app.post('/api/v1/parties',
                               data=self.new_parties_data_nonexisting_user)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Not Authorized")

    def test_get_specific_parties(self):
        result = self.app.get("/api/v1/parties/1")
        self.assertEqual(result.status_code, 200)
        data  = json.loads(result.data)
        self.assertEqual(data['data']["partiesId"], 1)

    def test_get_non_existing_record(self):
        result = self.app.get("/api/v1/parties/500")
        self.assertEqual(result.status_code, 404)

    def test_update_on_parties_headquaters(self):
        data = json.dumps({"userid": 1, "headquaters": "headquaters",})
        result = self.app.put('/api/v1/parties/1/headquaters', data=data)
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Cannot update a record not in draft state")

    def test_update_on_nonexisting_parties(self):
        data = json.dumps({"manifesto": "Peace",
                           "userid": 1})
        result = self.app.put('/api/v1/parties/500/manifesto', data=data)
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Update on non-existing record denied")
    
    def test_update_on_with_wrong_format(self):
        data = json.dumps({"manifesto": "Peace",
                          })
        result = self.app.put('/api/v1/parties/1/manifesto', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Manifesto/userid is not present")

    def test_update_with_empty_values(self):
        data = json.dumps({ })
        result = self.app.put('/api/v1/parties/1/parties', data=data)
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Page not found")

    def test_update_on_party_not_in_draft(self):
        data = json.dumps({"manifesto": "Peace",
                           "userid": 2})
        result = self.app.put('/api/v1/parties/2/manifesto', data=data)
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Cannot update a record not in draft state")

    def test_update_user_didnt_create_manifesto(self):
        data = json.dumps({"manifesto": "Peace",
                           "userid": 2})
        result = self.app.put('/api/v1/parties/1/manifesto', data=data)
        self.assertEqual(result.status_code, 403)

    def test_delete_parties(self):
        result = self.app.delete('/api/v1/parties/3',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(data["status"], 204)
        self.assertEqual(data['message'], "Parties record has been deleted")

    def test_delete_parties_with_wrong_user(self):
        result = self.app.delete('/api/v1/parties/2',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['message'], "Forbidden: Record not owned")

    def test_delete_nonexisting_parties(self):
        result = self.app.delete('/api/v1/parties/500',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['message'], "Party does not exist")
if __name__ == '__main__':
    unittest.main()
