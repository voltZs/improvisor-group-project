from flask_restful import Resource
from models.tag_model import TagModel 


class Tag(Resource):
    def get(self):
        return {"message" : "GET Request Received"}
    
    def post(self):
        return {"message" : "POST Request Received"}

class TagList(Resource):
    def get(self):
        pass