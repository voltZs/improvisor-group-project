from flask_restful import Resource
from models.tag_model import TagModel
from wtforms import Form, fields, validators
from forms import FormTag
from flask import request, redirect

class Tag(Resource):
    def get(self):
        return {"message" : "GET Request Received"}
    
    def post(self):
        print("POST on TAG ADD")
        form = FormTag(data=request.form)
        if form.validate():
            print("Valid form")
            return redirect("/")
        
        print("bad form")
        return {"message" : "bad form", "form" : form}

class TagList(Resource):
    def get(self):
        pass