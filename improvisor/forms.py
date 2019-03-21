from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, HiddenField, validators, PasswordField, RadioField


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

    assettype = RadioField('assettype', choices=[
        ('file','File'),
        ('link','Link')],
    default='file')

    assetResource = FileField("UPLOAD ASSET FILE:", validators=[
        # if we want to be able to upload a link this should probably be optional
        # FileRequired()
    ])

    assetLink = StringField('assetlink',validators=[
        validators.Optional(True),
        validators.Length(min=2, max=200)
    ])

    assetThumbnail = FileField("UPLOAD ASSET THUMBNAIL:", validators=[
        validators.Optional(True),
        FileAllowed(['jpg', 'png'])
    ])

    assetAutomaticThumbnail = HiddenField("This field should be hidden", validators=[
        validators.Optional(True)
    ])

class FormUpdateAsset(FlaskForm):
    assetname = StringField('assetname', validators=[
        validators.DataRequired(),
        validators.length(min=2, max =200)
    ])

    tagArrayString = StringField('tagArrayString', validators=[
        validators.DataRequired()
    ])
    


class FormLogin(FlaskForm):
    email = StringField('email', validators= [validators.Email()])
    password = PasswordField('password', validators=[
	    validators.DataRequired(),
		validators.Length(min=8, max=50)
	])

class FormSession(FlaskForm):
    sessionname = StringField('sessionname', validators= [
        validators.Length(min=1, max=50),
        validators.Regexp('/[A-Za-z]+$/', message="Session name must contain at least one character (A-Z)")
    ])

class FormUpdateSettings(FlaskForm):
    userPicture = FileField("UPLOAD PROFILE IMAGE:", validators=[
        validators.Optional(True),
        FileAllowed(['jpg', 'png'])
    ])
    passwordUpdate = PasswordField('Update Password', validators=[
		validators.Length(min=8, max=50),
        validators.Optional(True)
	])
    emailUpdate = StringField('Update Email', validators= [
        validators.Email(),
        validators.Optional(True)
    ])
