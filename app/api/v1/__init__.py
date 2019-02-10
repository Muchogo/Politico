from flask import Blueprint
from flask_restful import Api
from .views import (SignUpEndpoint, LoginEndpoint, AllPartiesEndpoint, PartiesEndpoint, PartiesEditManifestoEndpoint, PartiesEditHeadquatersEndpoint, AllAspirantsEndpoint, AspirantsEndpoint, AspirantsEditMemorandumEndpoint, AspirantsEditPartiesEndpoint)

v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(v1)
api.add_resource(SignUpEndpoint, '/signup')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(AllPartiesEndpoint, '/parties')
api.add_resource(PartiesEndpoint, '/parties/<int:parties_id>')
api.add_resource(PartiesEditManifestoEndpoint, '/parties/<int:parties_id>/manifesto')
api.add_resource(PartiesEditHeadquatersEndpoint, '/parties/<int:parties_id>/headquaters')
api.add_resource(AllAspirantsEndpoint, '/aspirants')
api.add_resource(AspirantsEndpoint, '/aspirants/<int:aspirants_id>')
api.add_resource(AspirantsEditMemorandumEndpoint, '/aspirants/<int:aspirants_id>/memorandum')
api.add_resource(AspirantsEditPartiesEndpoint, '/aspirants/<int:aspirants_id>/parties')

