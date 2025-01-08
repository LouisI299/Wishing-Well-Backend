#Configuration for the database
class Config:
    SECRET_KEY="secretkey"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False