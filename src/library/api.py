from library_database import Database
from library_list import Library
from library_asset import Asset
from loguru import logger
import sys


#Loguru config
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

path = "./media/database.db"
db = Database(path)
library = Library(db)
asset = Asset(db)


def add_asset(name, image=None, mesh=None, description=None):
    asset.add(name, image, mesh, description)

def update_asset(name, image=None, mesh=None, description=None):
    asset.update(name, image, mesh, description)

def delete_asset(name):
    asset.delete(name)

def list_asset():
    return library.get_list()
