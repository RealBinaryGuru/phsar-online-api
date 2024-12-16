import os
from dotenv import load_dotenv

load_dotenv()


class Environment():

    def __init__(self):
        self.DATABASE_URL = os.environ.get("DATABASE_URL")
