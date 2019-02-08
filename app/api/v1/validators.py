
from marshmallow import ValidationError, Schema, fields, ValidationError


def validate_string(s):

    if not s.strip():
        raise ValidationError('Empty string invalid')


class PartiesSchema(Schema):

    partiesId = fields.Int()
    createdOn = fields.DateTime()
    createdBy = fields.Int(required=True)
    headquaters = fields.Str(required=True)
    manifesto = fields.Str(required=True)
    status = fields.Str()
    images = fields.List(fields.Str())
    videos = fields.List(fields.Str())


class AspirantsSchema(Schema):

    aspirantsId = fields.Int()
    createdOn = fields.DateTime()
    createdBy = fields.Int(required=True)
    parties = fields.Str(required=True)
    memorandum = fields.Str(required=True)
    status = fields.Str()
    images = fields.List(fields.Str())
    videos = fields.List(fields.Str())


class UserSchema(Schema):

    userid = fields.Int()
    first_name = fields.Str(required=True, validate=validate_string)
    last_name = fields.Str(required=True, validate=validate_string)
    other_names = fields.Str(validate=validate_string)
    phonenumber = fields.Str(required=True, validate=validate_string)
    username = fields.Str(required=True, validate=validate_string)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate_string)
    isAdmin = fields.Bool()
    registeredOn = fields.DateTime()


class PartiesEditSchema(Schema):
    userid = fields.Int(required=True)
    manifesto = fields.Str(required=True)
    headquaters = fields.Str(required=True)

class AspirantsEditSchema(Schema):
    userid = fields.Int(required=True)
    memorandum = fields.Str(required=True)
    parties = fields.Str(required=True)