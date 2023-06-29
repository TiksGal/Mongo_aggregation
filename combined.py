from typing import Dict, Any
import logging
import logging.config
from pymongo.errors import PyMongoError, OperationFailure
from pymongo import MongoClient
from pymongo.cursor import Cursor
from utilities import execute_with_retry, set_validation_rules
from validation_sch import EMPLOYEES_VALIDATION_RULES

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


class Group:
    def __init__(self, host: str, port: int, db_name: str) -> None:
        client = MongoClient(host, port)
        self.db = client[db_name]

    def group_documents(
        self, collection_name: str, group_criteria: Dict[str, Any]
    ) -> Cursor:
        try:
            collection = self.db[collection_name]
            set_validation_rules(self.db, collection, EMPLOYEES_VALIDATION_RULES)
            pipeline = [{"$group": group_criteria}]
            return execute_with_retry(collection.aggregate, pipeline)
        except OperationFailure as e:
            logger.error(e)
        except PyMongoError as e:
            logger.error(e)


if __name__ == "__main__":
    group = Group("localhost", 27017, "Office")

    grouping: Dict[str, Any] = {
        "_id": "$work_position",
        "count": {"$sum": 1},
        "average_salary": {"$avg": "$salary"},
    }

    if cursor_object := group.group_documents(
        collection_name="emplloyees", group_criteria=grouping
    ):
        for doc in cursor_object:
            print(doc)


