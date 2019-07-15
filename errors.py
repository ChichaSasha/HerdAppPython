from werkzeug.exceptions import BadRequest, NotFound


class InvalidQueryParam(BadRequest):
    def __init__(self, err):
        BadRequest.__init__(self, "Invalid query param: {}".format(err))


class InvalidJson(BadRequest):
    def __init__(self, err):
        BadRequest.__init__(self, "Invalid json: {}".format(str(err)))


class EventNotFound(NotFound):
    def __init__(self, oid):
        NotFound.__init__(self, "Event {} not found".format(oid))


