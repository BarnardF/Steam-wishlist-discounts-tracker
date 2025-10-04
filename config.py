import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    STEAM_ID = os.getenv('STEAM_ID')
    DEBUG = True