from flask import Flask, jsonify, request, abort, json
import werkzeug
import datetime

from storage import Storage
from action import Action
from errors import *

app = Flask(__name__)

storage = Storage()


@app.route('/v1/events/ping', methods=["GET"])
def ping():
    return "Ok", 200


@app.route('/v1/events/<int:id>', methods=["GET"])
def get_by_id(id):
    res = storage.get_action_by_id(id)
    if res == 'not fund':
        return res, 404
    return res, 200


@app.route('/v1/events/', methods=["GET"])
def get_list_from_to():
    try:
        start_time = datetime.datetime.strptime(request.args["start_time"], "%Y-%m-%d").date()
        end_time = datetime.datetime.strptime(request.args["end_time"], "%Y-%m-%d").date()
    except ValueError as err:
        raise InvalidQueryParam("ValueError: {}".format(err))
    except KeyError as err:
        raise InvalidQueryParam("KeyError: {}".format(err))

    events = storage.get_list_from_to(start_time, end_time)

    return jsonify(start_time=str(start_time), end_time=str(end_time), events=[p.to_json() for p in events]), 200


@app.route('/v1/events/', methods=['POST'])
def add_action():
    if not request.json:
        abort(400)
    act = Action.from_json(request.json)
    storage.add_action(act)
    return act.to_json(), 200


@app.route('/v1/events/<int:id>', methods=['DELETE'])
def del_action(id):
    storage.del_action_by_id(id)
    return 200


@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    app.run()

