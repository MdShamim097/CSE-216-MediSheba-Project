import json


class JsonExtractor:
    def __init__(self, string):
        self.string = string

    def extract(self, file_location):
        dicts = []
        key_type = self.string
        file = open(file_location)
        data = json.load(file)
        for i in data:
            dicts.append(i[key_type])
        return dicts
