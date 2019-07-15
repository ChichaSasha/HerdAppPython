import datetime
from errors import *

class Action:
    def __init__(self, id, name, description, start_time, days_counter):
        self.id = id
        self.name = name
        self.description = description
        self.start_time = start_time
        self.days_counter = days_counter

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_time': self.start_time.strftime("%Y-%m-%d"),
            'days_counter': self.days_counter
        }

    @staticmethod
    def from_json(json):
        if "id" in json:
            oid = json["id"]
        else:
            oid = None

        try:
            name = json["name"]
            description = json.get("description", "")
            start_time = datetime.datetime.strptime(json["start_time"], "%Y-%m-%d").date()
            days_counter = json["days_counter"]

            return Action(oid, name, description, start_time, days_counter)

        except ValueError as err:
            raise InvalidJson("ValueError: {}".format(err))
        except KeyError as err:
            raise InvalidJson("KeyError: {}".format(err))

