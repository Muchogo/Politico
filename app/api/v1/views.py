

from flask import make_response, jsonify, request
from flask_restful import Resource
from .models import UserModel, PartiesModel, AspirantsModel

from .validators import (UserSchema, PartiesSchema,
                         PartiesEditSchema, AspirantsSchema, AspirantsEditSchema)


class SignUpEndpoint(Resource, UserModel):
    

    def __init__(self):
        self.user = UserModel()

    def post(self):
        
        data = request.get_json(force=True)
        user_data, error = UserSchema().load(data)

        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)

        if self.user.check_username(user_data['username']):
            return make_response(jsonify({"message": "Username already exists"}), 400)
        if self.user.check_email(user_data['email']):
            return make_response(jsonify({"message": "Email already exists"}), 400)

        if 'isAdmin' in user_data:
            self.user.save(
                user_data['first_name'],
                user_data['last_name'],
                user_data['other_names'],
                user_data['phonenumber'],
                user_data['email'],
                user_data['username'],
                user_data["password"],
                user_data['isAdmin']
            )
        else:
            self.user.save(
                user_data['first_name'],
                user_data['last_name'],
                user_data['other_names'],
                user_data['phonenumber'],
                user_data['email'],
                user_data['username'],
                user_data["password"]
            )

        return make_response(jsonify({"message": "Sign Up successful. Welcome!"}), 201)


class LoginEndpoint(Resource, UserModel):
    

    def __init__(self):
        self.users = UserModel()

    def post(self):

        data = request.get_json(force=True)
        user_data, error = UserSchema(
            only=('username', 'password')).load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)
        if self.users.confirm_login(user_data['username'], user_data['password']):
            return make_response(jsonify({"message": "Login Success!"}), 200)

        return make_response(jsonify({"message": "Login Failed!"}), 401)


class BasePartiesEndpoint(Resource, PartiesModel, UserModel):

    def __init__(self):
        self.db = PartiesModel()
        self.user = UserModel()


class AllPartiesEndpoint(BasePartiesEndpoint):

    def get(self):
        
        return make_response(jsonify(self.db.db), 200)

    def post(self):

        data = request.get_json(force=True)
        parties_data, error = PartiesSchema().load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)
        if self.user.search_user(parties_data['createdBy']):
            new_party = self.db.save( data["manifesto"], data['headquaters'],
                                        data['createdBy'], data['images'], data['videos'])
            return make_response(jsonify({"message": "New party created",
                                          "data": new_party}), 201)

        return make_response(jsonify({"message": "Not Authorized"}), 401)


class PartiesEndpoint(BasePartiesEndpoint):

    def get(self, parties_id):

        if self.db.db:
            result = self.db.search_parties(parties_id)
            if result is not None:
                return make_response(jsonify({"data": result}), 200)
            return make_response(jsonify({"message": "Party does not exist"}), 404)

        return make_response(jsonify({"message": "No Party created yet!"}), 200)

    def delete(self, parties_id):

        data = request.get_json(force=True)
        parties_data = PartiesEditSchema(
            only=('userid',)).load(data)
        if parties_data.errors:
            return make_response(jsonify({
                "message": "Missing userid field",
                "required": parties_data.errors,
                "status": 400}), 400)
        result = self.db.search_parties(parties_id)

        if result is not None:
            user = self.user.search_user(data['userid'])
            if user is not None and user['userid'] == result['createdBy']:
                parties_to_pop = self.db.db.index(result)
                self.db.db.pop(parties_to_pop)
                return make_response(jsonify({
                    "message": "Parties record has been deleted",
                    "status": 204,
                    "id": parties_id}), 200)

            return make_response(jsonify({"message": "Forbidden: Record not owned",
                                          "status": 403}), 403)

        return make_response(jsonify({
            "message": "Party does not exist",
            "status": 404
        }), 404)


class PartiesEditManifestoEndpoint(BasePartiesEndpoint):

    def put(self, parties_id):

        data = request.get_json(force=True)
        parties_data = PartiesEditSchema(
            only=('userid', 'manifesto')).load(data)
        if parties_data.errors:
            return make_response(jsonify({
                "message": "Manifesto/userid is not present",
                "required": parties_data.errors}),
                400)

        result = self.db.search_parties(parties_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['manifesto'] = data['manifesto']
                    return make_response(jsonify({
                        'message': "Parties Updated",
                        "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)


class PartiesEditHeadquatersEndpoint(BasePartiesEndpoint):

    def put(self, parties_id):

        data = request.get_json(force=True)
        parties_data = PartiesEditSchema(
            only=('userid', 'headquaters')).load(data)
        if parties_data.errors:
            return make_response(jsonify({
                "message": "headquaters/userid is not present",
                "required": parties_data.errors}),
                400)
        result = self.db.search_parties(parties_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['headquaters'] = data['headquaters']
                    return make_response(jsonify({
                        'message': "Parties Updated", "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)


class BaseAspirantsEndpoint(Resource, AspirantsModel, UserModel):

    def __init__(self):
        self.db = AspirantsModel()
        self.user = UserModel()


class AllAspirantsEndpoint(BaseAspirantsEndpoint):

    def get(self):
        
        return make_response(jsonify(self.db.db), 200)

    def post(self):

        data = request.get_json(force=True)
        aspirants_data, error = AspirantsSchema().load(data)
        if error:
            return make_response(jsonify({
                "message": "Missing or invalid field members",
                "required": error}), 400)
        if self.user.search_user(aspirants_data['createdBy']):
            new_aspirant = self.db.save( data["memorandum"], data['parties'],
                                        data['createdBy'], data['images'], data['videos'])
            return make_response(jsonify({"message": "New aspirant created",
                                          "data": new_aspirant}), 201)

        return make_response(jsonify({"message": "Not Authorized"}), 401)


class AspirantsEndpoint(BaseAspirantsEndpoint):

    def get(self, aspirants_id):

        if self.db.db:
            result = self.db.search_aspirants(aspirants_id)
            if result is not None:
                return make_response(jsonify({"data": result}), 200)
            return make_response(jsonify({"message": "Aspirant does not exist"}), 404)

        return make_response(jsonify({"message": "No Aspirants created yet!"}), 200)

    def delete(self, aspirants_id):

        data = request.get_json(force=True)
        aspirants_data = AspirantsEditSchema(
            only=('userid',)).load(data)
        if aspirants_data.errors:
            return make_response(jsonify({
                "message": "Missing userid field",
                "required": aspirants_data.errors,
                "status": 400}), 400)
        result = self.db.search_aspirants(aspirants_id)

        if result is not None:
            user = self.user.search_user(data['userid'])
            if user is not None and user['userid'] == result['createdBy']:
                parties_to_pop = self.db.db.index(result)
                self.db.db.pop(parties_to_pop)
                return make_response(jsonify({
                    "message": "Aspirants record has been deleted",
                    "status": 204,
                    "id": aspirants_id}), 200)

            return make_response(jsonify({"message": "Forbidden: Record not owned",
                                          "status": 403}), 403)

        return make_response(jsonify({
            "message": "Aspirant does not exist",
            "status": 404
        }), 404)


class AspirantsEditMemorandumEndpoint(BaseAspirantsEndpoint):

    def put(self, aspirants_id):

        data = request.get_json(force=True)
        aspirants_data = AspirantsEditSchema(
            only=('userid', 'memorandum')).load(data)
        if aspirants_data.errors:
            return make_response(jsonify({
                "message": "Memorandum/userid is not present",
                "required": aspirants_data.errors}),
                400)

        result = self.db.search_aspirants(aspirants_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['memorandum'] = data['memorandum']
                    return make_response(jsonify({
                        'message': "Aspirants Updated",
                        "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)


class AspirantsEditPartiesEndpoint(BaseAspirantsEndpoint):

    def put(self, aspirants_id):

        data = request.get_json(force=True)
        aspirants_data = AspirantsEditSchema(
            only=('userid', 'parties')).load(data)
        if aspirants_data.errors:
            return make_response(jsonify({
                "message": "parties/userid is not present",
                "required": aspirants_data.errors}),
                400)
        result = self.db.search_aspirants(aspirants_id)
        if result is not None:
            if result['status'] == 'draft':
                user = self.user.search_user(data['userid'])
                if user is not None and user['userid'] == result['createdBy']:
                    result['parties'] = data['parties']
                    return make_response(jsonify({
                        'message': "Aspirants Updated", "data": result}), 200)

                return make_response(jsonify({
                    "message": "Forbidden: Record not owned"}), 403)

            return make_response(jsonify({
                "message": "Cannot update a record not in draft state"}), 403)

        return make_response(jsonify({
            "message": "Update on non-existing record denied"}), 404)

