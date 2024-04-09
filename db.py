from pymongo import MongoClient
import config
import os

#Conection to MongoDB and selecting database.
collection_name="studentDB"
try:

    cli = MongoClient(os.environ['DATABASE_URL'])
    db = cli['studentcol']  # If there is Database it will get selected or else this step will create database

    #If collection already exists else create the collection based on below schema

    if len(db.list_collection_names()) == 0:
        try:
            db.create_collection(collection_name, validator={'$jsonSchema': {'bsonType': 'object', 'required': ['name', 'age', 'address'], 'properties': {'name': {'bsonType': 'string'}, 'age': {'bsonType': 'int'}, 'address': {'bsonType': 'object', 'required': ['city', 'country'], 'properties': {'city': {'bsonType': 'string'}, 'country': {'bsonType': 'string'}}}}}})
            print("collection created")

        except Exception as err:
            f"Collection was not created due to some error: {err}"
    else:
        print("collection is already created")

    
except Exception as err:
    f"Database not connected due to: {err}"

students_collection=db[collection_name]
print("success")


