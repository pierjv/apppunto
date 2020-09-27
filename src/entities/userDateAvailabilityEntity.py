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

class userDateAndHourAvailabilityEntity:
    def __init__(self,id_user= None, id_type_availability = None, full_name = None,date_availability = None,
                hours_availability = None, enable = None):
        self.id_user = id_user
        self.id_type_availability = id_type_availability
        self.full_name = full_name
        self.date_availability = date_availability
        self.enable = enable
        self.hours_availability  = hours_availability

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
        
        _date_availability = values.date_availability
        _full_name = values.full_name
        _id_type_availability = values.id_type_availability
        _id_user = values.id_user
        _enable = 1

        _user_date_availabilities =[]
        if (len(values.hours_availability)>=1):
            for us in values.hours_availability:
                _entity = userDateAvailabilityEntity()
                _entity.id_user = _id_user
                _entity.id_type_availability = _id_type_availability
                _entity.full_name = _full_name
                _entity.date_availability = _date_availability
                _entity.hour_availability = us
                _entity.enable = _enable
                _user_date_availabilities.append(_entity)
        else:
                _entity = userDateAvailabilityEntity()
                _entity.id_user = _id_user
                _entity.id_type_availability = _id_type_availability
                _entity.full_name = _full_name
                _entity.date_availability = _date_availability
                _entity.hour_availability = 0
                _entity.enable = _enable
                _user_date_availabilities.append(_entity)


        self.user_date_availabilities = _user_date_availabilities
