from Action import Action
from DateTime import DateTime

class Actions:
    def __init__(self):
        self.acts = []
        self.every_day_acts = []
        self.single_acts = []
        self.not_every_day_acts = []

    def add_action(self, some_action):
        self.acts.append(some_action)
        if some_action.days_counter > 1:
            self.not_every_day_acts.append(some_action)
        elif some_action.days_counter == 1:
            self.every_day_acts.append(some_action)
        else:
            self.single_acts.append(some_action)

    def get_list_from_to(self, start_time, end_time):
        start_time = DateTime(start_time)
        end_time = DateTime(end_time)
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
                        a = Action(self.every_day_acts[k].name, self.every_day_acts[k].id, i,
                                   self.every_day_acts[k].description, self.every_day_acts[k].days_counter)
                        res.append(a)
                        i += 1
                    k += 1
            elif (obj.start_time > start_time) and (obj.start_time < end_time):
                k = 0
                while k < len(self.every_day_acts):
                    i = start_time
                    while i < end_time:
                        a = Action(self.every_day_acts[k].name, self.every_day_acts[k].id, i,
                                   self.every_day_acts[k].description, self.every_day_acts[k].days_counter)
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
                                a = Action(self.not_every_day_acts[k].name, self.not_every_day_acts[k].id,
                                           self.not_every_day_acts[k].description,
                                           i, self.not_every_day_acts[k].days_counter)
                                res.append(a)
                            i += 1
                        k += 1
                elif (obj.start_time > start_time) and (obj.start_time < end_time):
                    while k < len(self.not_every_day_acts):
                        i = start_time
                        while i < end_time:
                            diff = i - self.not_every_day_acts[k].start_time
                            if diff % self.not_every_day_acts[k].days_counter == 0:
                                a = Action(self.not_every_day_acts[k].name, self.not_every_day_acts[k].id,
                                           self.not_every_day_acts[k].description,
                                           i, self.not_every_day_acts[k].days_counter)
                                res.append(a)
                            i += 1
                        k += 1
        print(res)
        return sorted(res, key=lambda action: action.start_time)

    def get_action_by_id(self, some_id):
        for i in self.acts:
            if i.id == some_id:
                return i.to_json()
        return "not fund"

    def del_action_by_id(self, some_id):
        if some_id == 100:
            return "Can`t be deleted"
        for i in self.acts:
            if i.id == some_id:
                self.acts = [action for action in self.acts if action.id != some_id]
                if i.days_counter == 1:
                    self.every_day_acts = [action for action in self.every_day_acts if action.id != some_id]
                elif i.days_counter > 1:
                    self.not_every_day_acts = [action for action in self.not_every_day_acts if action.id != some_id]
                else:
                    self.single_acts = [action for action in self.single_acts if action.id != some_id]
                return "{} is deleted.".format(some_id)

        return "{} is not in list.".format(some_id)
