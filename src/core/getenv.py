import os

from dotenv import load_dotenv

load_dotenv()


class Environment():

    def __init__(self):
        self.DATABASE_URL = os.environ.get("DATABASE_URL")
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.ALGORITHM = os.environ.get("ALGORITHM")
        self.TOKEN_EXPIRE = int(os.environ.get("TOKEN_EXPIRE"))
