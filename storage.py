from action import Action
from errors import *
import copy

actions_id_counter = 100


def get_next_id():
    global actions_id_counter
    actions_id_counter += 1
    return actions_id_counter


class Storage:
    def __init__(self):
        self.acts = []

    def add_action(self, some_action):
        some_action.id = get_next_id() # new action, generate new id

        self.acts.append(some_action)

    def get_action_by_id(self, some_id):
        for p in self.acts:
            if p.id == some_id:
                return p.to_json()

        raise EventNotFound(some_id)

    def del_action_by_id(self, some_id):
        for i in self.acts:
            if i.id == some_id:
                self.acts = [action for action in self.acts if action.id != some_id]
                return

        raise EventNotFound(some_id)

    def get_not_every_day_acts(self):
        return [event for event in self.acts if event.days_counter > 1]

    def get_every_day_acts(self):
        return [event for event in self.acts if event.days_counter == 1]

    def get_single_acts(self):
        return [event for event in self.acts if event.days_counter == 0]


class Handler():

    def init(self,storage):
        self.storage = storage
        self.not_every_day_acts = self.storage.get_not_every_day_acts()
        self.every_day_acts = self.storage.get_every_day_acts()
        self.single_day_acts = self.storage.get_single_acts()

    def get_list_from_to(self,start_time,end_time):
            res = []
            for i in self.single_acts:
                if (i.start_time > start_time) and (i.start_time < end_time):
                    res.append(i)

            for obj in self.every_day_acts:

                if obj.start_time < start_time:
                    k = 0
                    while k < len(self.every_day_acts):
                        i = start_time
                        while i < end_time:
                            a = copy.copy(self.every_day_acts[k])  # true way
                            a.start_time = i
                            res.append(a)
                            i += 1
                        k += 1
                elif (obj.start_time > start_time) and (obj.start_time < end_time):
                    k = 0
                    while k < len(self.every_day_acts):
                        i = start_time
                        while i < end_time:
                            a = copy.copy(self.every_day_acts[k])  # true way
                            a.start_time = i
                            res.append(a)
                            i += 1
                        k += 1
                k = 0
                for obj in self.not_every_day_acts:
                    if obj.start_time < start_time:
                        while k < len(self.not_every_day_acts):
                            i = start_time
                            while i < end_time:
                                diff = i - self.not_every_day_acts[k].start_time

                                if diff % self.not_every_day_acts[k].days_counter == 0:
                                    a = copy.copy(self.every_day_acts[k])  # true way
                                    a.start_time = i
                                    res.append(a)
                                i += 1
                            k += 1
                    elif (obj.start_time > start_time) and (obj.start_time < end_time):
                        while k < len(self.not_every_day_acts):
                            i = start_time
                            while i < end_time:
                                diff = i - self.not_every_day_acts[k].start_time
                                if diff % self.not_every_day_acts[k].days_counter == 0:
                                    a = copy.copy(self.every_day_acts[k])  # true way
                                    a.start_time = i
                                    res.append(a)
                                i += 1
                            k += 1

            return sorted(res, key=lambda action: action.start_time)



