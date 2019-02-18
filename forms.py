from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, PasswordField


class FormTag(FlaskForm):
    tag = StringField('tag', [
        validators.DataRequired()
    ])
    user_id = IntegerField('user_id', [
        validators.DataRequired()
    ])

# Not implemented yet but will be useful for user signup form
class FormSignup(FlaskForm):
    firstname = StringField('firstname', [
	    validators.Length(min=2, max=50),
		validators.Regexp('^\\w+$', message="First name may only contain letters")
		])
    lastname = StringField('lastname', [
	    validators.Length(min=2, max=50),
		validators.Regexp('^\\w+$', message="Last name may only contain letters")
		])
    email = StringField('email', [validators.Email()])
    password = PasswordField('password', [
		validators.DataRequired(),
		validators.Length(min=8, max=15, message="Password must be between 8 and 15 characters long inclusive"),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
    confirm = PasswordField('confirm')

class FormAsset(FlaskForm):
    assetname = StringField('assetname', [
        validators.Length(min=2, max=200)
    ])

class FormLogin(FlaskForm):
    email = StringField('email', [validators.Email()])
    password = PasswordField('password', [
	    validators.DataRequired(),
		validators.Length(min=8, max=15, message="Password must be between 8 and 15 characters long inclusive"),
		validators.EqualTo('confirm', message='Passwords do not match')
	])