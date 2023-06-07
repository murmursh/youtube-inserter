import json

class JsonSafeDictMethod:
    def __safe_dict__(self):
        """
        This method returns a dictionary containing the public attributes
        of the instance. This method is intended to be used by the `to_json`
        method to serialize the instance to a JSON object.
        """
        safe_dict = {}
        for key, value in self.__dict__.items():
            # Ignore private and protected attributes
            if not key.startswith("_"):
                # Check if the value can be serialized to JSON
                try:
                    json.dumps(value)
                except TypeError:
                    continue
                safe_dict[key] = value
        return safe_dict
    
    def to_json(self):
        """
        This method returns a JSON string representing the instance. The
        JSON object only contains the public attributes of the instance.
        """
        safe_dict = self.__safe_dict__()
        json_string = json.dumps(safe_dict)
        return json_string
    
    def to_json_file(self, path:str):
        """
        This method creates a JSON file representing the instance. The
        JSON object only contains the public attributes of the instance.
        """
        safe_dict = self.__safe_dict__()
        with open(path, 'w') as f:
            json.dump(safe_dict, f)

    @classmethod
    def from_json(cls, json_string):
        """
        This class method creates a new instance of the class from a JSON
        string. The JSON object should only contain public attributes of the
        instance. Private and protected attributes will not be restored.
        """
        data = json.loads(json_string)
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    def _from_json(self, json_string):
        """
        This class method creates a new instance of the class from a JSON
        string. The JSON object should only contain public attributes of the
        instance. Private and protected attributes will not be restored.
        """
        data = json.loads(json_string)
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def from_json_file(cls, fp):
        """
        This class method creates a new instance of the class from a JSON
        string. The JSON object should only contain public attributes of the
        instance. Private and protected attributes will not be restored.
        """
        with open(fp, "r") as f:
            data = json.load(f)
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    def _from_json_file(self, fp):
        """
        This class method creates a new instance of the class from a JSON
        string. The JSON object should only contain public attributes of the
        instance. Private and protected attributes will not be restored.
        """
        with open(fp, "r") as f:
            data = json.load(f)
        for key, value in data.items():
            setattr(self, key, value)