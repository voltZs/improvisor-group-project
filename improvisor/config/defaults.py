# Datebase connection info
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI =  "sqlite:///data.db"
PROPAGATE_EXCEPTIONS = True
# Secret key
SECRET_KEY = "b'\\x01IO\\x08\\x08L\\xe8Nia5\\x82\\x98\\xa5\\xc6\\xd3\\xf1\\xcf`\\xa3\\xb8G4\\xf8"
# File upload size limit (32MB)
MAX_CONTENT_LENGTH = 32 * 1024 * 1024
# Mail client configuration
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
# Mail login info
MAIL_USERNAME = "noreply.improvisor@gmail.com"
MAIL_PASSWORD = "QqXmgyw83CJZVccf4TBrL9sKV"