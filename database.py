from pyArango.connection import Connection
from pyArango.collection import Collection, Field
from pyArango.theExceptions import CreationError
from dotenv import dotenv_values

config = dotenv_values(".env")

class ArtistsCollection(Collection):
    _properties = {
        "keyOptions": {
            "allowUserKeys": True,
            "type": "traditional"
        }
    }

def init_database():
    conn = Connection(
        arangoURL=config["ARANGO_URL"],
        username=config["ARANGO_USERNAME"],
        password=config["ARANGO_PASSWORD"]
    )
    
    # Create database if it doesn't exist
    db_name = config["ARANGO_DB"]
    if not conn.hasDatabase(db_name):
        db = conn.createDatabase(name=db_name)
    else:
        db = conn[db_name]
    
    # Create collection if it doesn't exist
    if not db.hasCollection("artists"):
        db.createCollection("ArtistsCollection")
    
    return conn, db