from pymongo.errors import PyMongoError, OperationFailure
from typing import Dict, Any
from pymongo.cursor import Cursor
from utilities import execute_with_retry, connect_to_db
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


class Sort:
    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.db = connect_to_db(host, port, db_name)

    def sort_documents(
        self, collection_name: str, sort_criteria: Dict[str, Any]
    ) -> Cursor:
        try:
            collection = self.db[collection_name]
            pipeline = [{"$sort": sort_criteria}]
            return execute_with_retry(collection.aggregate, pipeline)
        except (PyMongoError, OperationFailure) as e:
            logger.error(e)


if __name__ == "__main__":
    sort = Sort("localhost", 27017, "Office")

    if cursor_object := sort.sort_documents(
        collection_name="emplloyees", sort_criteria={"salary": 1}
    ):
        for doc in cursor_object:
            print(doc)