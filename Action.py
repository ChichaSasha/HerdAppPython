from DateTime import *

global_id = 101


class Action:
    def __init__(self, name, id, description, start_time, days_counter):
        self.name = name
        self.id = id
        self.description = description
        self.start_time = start_time
        self.days_counter = days_counter

    def to_json(self):
        return {'name': str(self.name),
                'id': str(self.id),
                'description': str(self.description),
                'start_time': str(self.start_time),
                'days_counter': str(self.days_counter),
                }

    @staticmethod
    def from_json(json):
        global global_id
        global_id += 1
        name = json["name"]
        id = global_id
        description = json["description"]
        start_time = DateTime(json["start_time"])
        days_counter = json["days_counter"]
        act = Action(name, id, description, start_time, days_counter)
        return act
