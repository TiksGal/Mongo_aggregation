EMPLOYEES_VALIDATION_RULES = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "age", "city", "salary", "work_position"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "name must be a string and is required"
                },
                "age": {
                    "bsonType": "int",
                    "minimum": 0,
                    "maximum": 120,
                    "description": "age must be an integer in [0, 120] and is required"
                },
                "city": {
                    "bsonType": "string",
                    "description": "city must be a string and is required"
                },
                "salary": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "salary must be a non-negative integer and is required"
                },
                "work_position": {
                    "bsonType": "string",
                    "description": "work_position must be a string and is required"
                },
            },
        }
    }
}
