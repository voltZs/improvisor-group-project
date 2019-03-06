from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, validators, PasswordField


class FormTag(FlaskForm):
    tag = StringField('tag', [
        validators.DataRequired()
    ])
    
class FormSignup(FlaskForm):
    firstname = StringField('firstname', [
	    validators.Length(min=2, max=50),
		validators.Regexp('^\\w+$', message="First name may only contain letters")
		])
    lastname = StringField('lastname', [
        validators.Length(min=2, max=50),
		validators.Regexp('^\\w+$', message="Last name may only contain letters")
		])
    email = StringField('email', [validators.Email()
        ])
    password = PasswordField('password', [
		validators.DataRequired(),
		validators.Length(min=8, max=50)
		])

class FormAsset(FlaskForm):
    assetname = StringField('assetname', [
        validators.Length(min=2, max=200)
    ])
    tagname = StringField('tagname',[
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


class FormLogin(FlaskForm):
    email = StringField('email', [validators.Email()])
    password = PasswordField('password', [
	    validators.DataRequired(),
		validators.Length(min=8, max=50)
	])

class FormProfilePicture(FlaskForm):
    userPicture = FileField("UPLOAD PROFILE IMAGE:", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'])
    ])
    password = PasswordField('password', [
		validators.Length(min=8, max=50),
        validators.Optional(True)
	])
    email = StringField('email', [
        validators.Email(),
        validators.Optional(True)
    ])