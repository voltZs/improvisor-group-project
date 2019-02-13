from flask_wtf import FlaskForm
from wtforms import StringField, validators


class FormTag(FlaskForm):
    tag = StringField('tag', [
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