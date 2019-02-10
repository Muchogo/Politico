
import datetime

USER_DB = []


class UserModel():

    def __init__(self):
        self.db = USER_DB
        self.save(
            first_name="Eric",
            last_name="Muchogo",
            other_names="Ndungu",
            phonenumber="0725530122",
            email="erimucho@gmail.com",
            username="Muchogo",
            password="1000",
            isAdmin=True
        )

    def save(self, first_name, last_name, other_names, phonenumber,
             email, username, password, isAdmin=False):

        data = {
            "userid": len(self.db) + 1,
            "first_name": first_name,
            "last_name": last_name,
            "other_names": other_names,
            "phonenumber": phonenumber,
            "username": username,
            "email": email,
            "password": password,
            "isAdmin": isAdmin,
            "registeredOn": datetime.datetime.now(),
        }
        self.db.append(data)
        return data

    def check_username(self, username):
        return next(filter(lambda x: x['username'] == username, self.db), None)

    def check_email(self, email):
        return next(filter(lambda x: x['email'] == email, self.db), None)

    def confirm_login(self, username, pwd):
        return next(filter(lambda x: x['username'] == username and x['password'] == pwd, self.db), None)

    def search_user(self, id):
        return next(filter(lambda u: u['userid'] == id, self.db), None)


PARTIES = [
    {
        "partiesId": 1,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "headquaters": "nairobi",
        "status": "approved",
        "manifesto": "Discussion of Flask",
        "images": ['https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?cs=srgb&dl=beach-exotic-holiday-248797.jpg&fm=jpg']
    },
    {
        "partiesId": 2,
        "createdOn": datetime.datetime.now(),
        "createdBy": 2,
        "headquaters": "mombasa",
        "status": "Cancelled",
        "manifesto": "Fellowship of Django",
        "images": []
    },
    {
        "partiesId": 3,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "headquaters": "nakuru",
        "status": "disputed",
        "manifesto": "Discussion on Agile",
        "images": []
    }
]

class PartiesModel():
    def __init__(self):
        self.db = PARTIES

    def save(self, manifesto, headquaters, createdBy, images, videos, status="draft"):
        uid = len(self.db) + 1
        data = {
            "partiesId": uid,
            "createdOn": datetime.datetime.now(),
            "createdBy": createdBy,
            "headquaters": headquaters,
            "status": status,
            "manifesto": manifesto,
            "images": images,
        }
        self.db.append(data)
        return data

    def search_parties(self, id):
        return next(filter(lambda i: i["partiesId"] == id, self.db), None)

ASPIRANTS = [
    {
        "aspirantsId": 1,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "parties": "DP",
        "status": "approved",
        "memorandum": "Discussion of Flask",
        "images": ['https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg?cs=srgb&dl=beach-exotic-holiday-248797.jpg&fm=jpg']
    },
    {
        "aspirantsId": 2,
        "createdOn": datetime.datetime.now(),
        "createdBy": 2,
        "parties": "URP",
        "status": "approved",
        "memorandum": "Fellowship of Django",
        "images": []
    },
    {
        "aspirantsId": 3,
        "createdOn": datetime.datetime.now(),
        "createdBy": 1,
        "parties": "CCM",
        "status": "disputed",
        "memoramdum": "Discussion on Agile",
        "images": []
    }
]

class AspirantsModel():
    def __init__(self):
        self.db = ASPIRANTS

    def save(self, memorandum, parties, createdBy, images, videos, status="draft"):
        uid = len(self.db) + 1
        data = {
            "aspirantsId": uid,
            "createdOn": datetime.datetime.now(),
            "createdBy": createdBy,
            "parties": parties,
            "status": status,
            "memorandum": memorandum,
            "images": images,
        }
        self.db.append(data)
        return data

    def search_aspirants(self, id):
        return next(filter(lambda i: i["aspirantsId"] == id, self.db), None)
    
