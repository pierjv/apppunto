import json
from collections import namedtuple

class userDateAvailabilityEntity:
    def __init__(self,id_user= None, id_type_availability = None, full_name = None,date_availability = None,
                hour_availability = None, enable = None,status = None):
        self.id_user = id_user
        self.id_type_availability = id_type_availability
        self.full_name = full_name
        self.date_availability = date_availability
        self.hour_availability  = hour_availability
        self.enable = enable
        self.status = status

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
class lstDateAvailabilityEntity:
    def __init__(self,user_date_availabilities= None):
        self.user_date_availabilities = user_date_availabilities

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    def requestToClass(self,resquest):
        data = resquest.get_json() 
        data = json.dumps(data)
        values = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        _user_date_availabilities =[]
        for us in values:
            print(us)
            _entity = userDateAvailabilityEntity()
            _entity.id_user = us.id_user
            _entity.id_type_availability = us.id_type_availability
            _entity.full_name = us.full_name
            _entity.date_availability = us.date_availability
            _entity.hour_availability = us.hour_availability
            _entity.enable = us.enable
            _user_date_availabilities.append(_entity)

        self.user_date_availabilities = _user_date_availabilities 
