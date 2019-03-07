from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, validators, PasswordField, RadioField


class FormTag(FlaskForm):
    tag = StringField('tag', validators=[
        validators.DataRequired()
    ])
    
class FormSignup(FlaskForm):
    firstname = StringField('firstname',validators= [
	    validators.Length(min=2, max=50),
		validators.Regexp('^\\w+$', message="First name may only contain letters")
		])
    lastname = StringField('lastname', validators=[
        validators.Length(min=2, max=50),
		validators.Regexp('^\\w+$', message="Last name may only contain letters")
		])
    email = StringField('email', validators=[validators.Email()
        ])
    password = PasswordField('password', validators=[
		validators.DataRequired(),
		validators.Length(min=8, max=50)
		])

class FormAsset(FlaskForm):
    assetname = StringField('assetname', validators= [
        validators.Length(min=2, max=200)
    ])
    tagname = StringField('tagname',validators=[
        validators.Optional(True),
        validators.Length(min=2,max=200)
    ])
    assetResource = FileField("UPLOAD ASSET FILE:", validators=[
        FileRequired()
    ])
    assetThumbnail = FileField("UPLOAD ASSET THUMBNAIL:", validators=[
        validators.Optional(True),
        FileAllowed(['jpg', 'png'])
    ])

class FormUpdateAsset(FlaskForm):
    tagname = StringField('tagname', validators=[
        validators.Optional(True),
        validators.Length(min=2, max=200)
    ])
    operation = RadioField("Delete or Add", choices =[("delete", "Delete Tag"), ("add", "Add Tag")], validators=[
        validators.DataRequired(message="choose to delete or add specified tag")
    ])
class FormLogin(FlaskForm):
    email = StringField('email', validators= [validators.Email()])
    password = PasswordField('password', validators=[
	    validators.DataRequired(),
		validators.Length(min=8, max=50)
	])

class FormProfilePicture(FlaskForm):
    userPicture = FileField("UPLOAD PROFILE IMAGE:", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'])
    ])
    password = PasswordField('password', validators=[
		validators.Length(min=8, max=50),
        validators.Optional(True)
	])
    email = StringField('email', validators= [
        validators.Email(),
        validators.Optional(True)
    ])