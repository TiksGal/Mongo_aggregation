from pymongo import MongoClient
from faker import Faker
import random

class ExampleCollection:
    def __init__(self, Office, emplloyees):
        self.collection = MongoClient('localhost', 27017)[Office][emplloyees]

    def insert_document(self, document):
        result = self.collection.insert_one(document)
        return result.inserted_id

# Instantiate Faker
fake = Faker()

# Define some example work positions
work_positions = ["Manager", "Engineer", "Clerk", "Salesperson", "Driver", "Maintenance", "HR"]

# Usage
example_collection = ExampleCollection("Office", "emplloyees")

for _ in range(20):
    document = {
        "name": fake.name(),
        "age": random.randint(20, 60),
        "city": fake.city(),
        "salary": random.randint(30000, 120000),
        "work_position": random.choice(work_positions)
    }
    document_id = example_collection.insert_document(document)
    print(f"Document inserted with ID: {document_id}")
