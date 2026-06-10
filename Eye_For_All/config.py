import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///osint.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')