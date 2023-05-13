#!/usr/bin/python3
"""implementation of class FileStorage"""

import json


class FileStorage:
    """serializes instances to a JSON file
        and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """this method return  of previously saved
            values  __objects a dictionary object
        """
        return (self.__objects)

    def new(self, obj):
        """enable __objects to uniquely store different
            obj address of isistance(BaseModel) as
            a value pair of  <obj class name>.id key
        """
        obj_key = "{}.{}".format((type(obj)).__name__, obj.id)
        self.__objects[obj_key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_data = {}
        with open(self.__file_path, 'w', encoding="utf-8") as f:
            for keys, vals in self.__objects.items():
                json_data[keys] = vals.to_dict()
            json.dump(json_data, f)

    def reload(self):
        """deserializes json file: __file_path to dictionary obj: __objects"""
        from models.base_model import BaseModel

        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                json_dict = json.load(f)
        # help all() to be able to return previous data assign to  __objects
                for keys, vals in json_dict.items():
                    self.__objects[keys] = BaseModel(**vals)
        except FileNotFoundError:
            pass
