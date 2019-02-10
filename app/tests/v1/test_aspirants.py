
import unittest
from flask import json
from ... import create_app
from .basetest import BaseTestCase
app = create_app()


class AspirantsTest(BaseTestCase):
 
    def test_create_new_aspirants(self):
        result = self.app.post('/api/v1/aspirants', data=self.new_aspirants)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "New aspirant created")

    def test_get_all_aspirants(self):
        result = self.app.get('/api/v1/aspirants')
        self.assertEqual(result.status_code, 200)

    def test_create_new_aspirants_user_doesnt_exist(self):
        result = self.app.post('/api/v1/aspirants',
                               data=self.new_aspirants_data_nonexisting_user)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Not Authorized")

    def test_get_specific_aspirants(self):
        result = self.app.get("/api/v1/aspirants/1")
        self.assertEqual(result.status_code, 200)
        data  = json.loads(result.data)
        self.assertEqual(data['data']["aspirantsId"], 1)

    def test_get_non_existing_record(self):
        result = self.app.get("/api/v1/aspirants/500")
        self.assertEqual(result.status_code, 404)

    def test_update_an_aspirants_parties(self):
        data = json.dumps({"parties": "ODM",
                           "userid": 1})
        result = self.app.put('/api/v1/aspirants/1/parties', data=data)
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Cannot update a record not in draft state")

    def test_update_on_nonexisting_aspirants(self):
        data = json.dumps({"memorandum": "Peace",
                           "userid": 1})
        result = self.app.put('/api/v1/aspirants/500/memorandum', data=data)
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Update on non-existing record denied")
    
    def test_update_on_with_wrong_format(self):
        data = json.dumps({"memorandum": "Peace",
                          })
        result = self.app.put('/api/v1/aspirants/1/memorandum', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Memorandum/userid is not present")

    def test_update_with_empty_values(self):
        data = json.dumps({})
        result = self.app.put('/api/v1/aspirants/1/parties', data=data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "parties/userid is not present")

    def test_update_on_aspirant_not_in_draft(self):
        data = json.dumps({"memorandum": "Peace",
                           "userid": 2})
        result = self.app.put('/api/v1/aspirants/2/memorandum', data=data)
        self.assertEqual(result.status_code, 403)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Cannot update a record not in draft state")

    def test_update_user_didnt_create_memorandum(self):
        data = json.dumps({"memorandum": "Peace",
                           "userid": 2})
        result = self.app.put('/api/v1/aspirants/1/memorandum', data=data)
        self.assertEqual(result.status_code, 403)

    def test_delete_aspirants(self):
        result = self.app.delete('/api/v1/aspirants/3',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(data["status"], 204)
        self.assertEqual(data['message'], "Aspirants record has been deleted")

    def test_delete_aspirants_with_wrong_user(self):
        result = self.app.delete('/api/v1/aspirants/2',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 403)
        self.assertEqual(data['message'], "Forbidden: Record not owned")

    def test_delete_nonexisting_aspirants(self):
        result = self.app.delete('/api/v1/aspirants/500',
                                 data=json.dumps({"userid": 1}))
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['message'], "Aspirant does not exist")
if __name__ == '__main__':
    unittest.main()
