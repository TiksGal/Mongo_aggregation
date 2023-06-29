from pymongo.errors import PyMongoError, OperationFailure
from typing import Dict, Any
from pymongo.cursor import Cursor
from utilities import execute_with_retry, connect_to_db
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


class Filter:
    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.db = connect_to_db(host, port, db_name)

    def filter_documents(
        self, collection_name: str, filter_criteria: Dict[str, Any]
    ) -> Cursor:
        try:
            collection = self.db[collection_name]
            pipeline = [{"$match": filter_criteria}]
            return execute_with_retry(collection.aggregate, pipeline)
        except (PyMongoError, OperationFailure) as e:
            logger.error(e)


if __name__ == "__main__":
    filter = Filter("localhost", 27017, "Office")

    if cursor_object := filter.filter_documents(
        collection_name="emplloyees", filter_criteria={"work_position": "Driver"}
    ):
        for doc in cursor_object:
            print(doc)