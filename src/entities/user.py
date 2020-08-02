import json

class userEntity:
    def __init__(self,name,code):
        self.name = name
        self.code = code

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)