from pymongo import MongoClient
from pymongo.errors import PyMongoError, OperationFailure
from typing import Dict, Any
from pymongo.cursor import Cursor
from utilities import execute_with_retry, connect_to_db
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


class Project:
    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.db = connect_to_db(host, port, db_name)

    def project_documents(
        self, collection_name: str, project_criteria: Dict[str, Any]
    ) -> Cursor:
        try:
            collection = self.db[collection_name]
            pipeline = [{"$project": project_criteria}]
            return execute_with_retry(collection.aggregate, pipeline)
        except (PyMongoError, OperationFailure) as e:
            logger.error(e)


if __name__ == "__main__":
    project = Project("localhost", 27017, "Office")

    if cursor_object := project.project_documents(
        collection_name="emplloyees", project_criteria={"name": 1, "age": 1, "city": 1, "salary": 1}
    ):
        for doc in cursor_object:
            print(doc)

