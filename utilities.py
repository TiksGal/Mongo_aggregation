from typing import Dict, Any
import logging
import logging.config
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


def connect_to_db(host: str, port: int, db_name: str) -> "Database":
    client = MongoClient(host, port)
    db = client[db_name]
    return db


def execute_with_retry(func, *args, **kwargs) -> None:
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            # Execute the provided function
            return func(*args, **kwargs)  # If execution is successful, exit the loop
        except ConnectionFailure as e:
            print(f"Execution failed: {e}")
            retries += 1
            print(f"Retrying... (Attempt {retries}/{max_retries})")
            logger.error(e)
    else:
        print("Maximum retries exceeded. Giving up.")
        
def set_validation_rules(
    db: Database, collection: Collection, validation_rules: Dict[str, Any]
) -> None:
    try:
        db.command("collMod", collection.name, **validation_rules)
    except OperationFailure as e:
        logger.error(e)
    except PyMongoError as e:
        logger.error(e)