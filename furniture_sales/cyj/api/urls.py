from api.resource import Api
from api.user import User_Login,User_Register

api = Api()
api.add_resource(User_Login())
api.add_resource(User_Register())

