from flask import Flask, jsonify, request, abort
from flask_restful import Api, reqparse
from DateTime import DateTime
from Action import *
from Actions import *
##test git
app = Flask(__name__)
api = Api(app)

admin = Action('Admin', 100, 'super tasty', DateTime(1970, 7, 10), 0)
actions = Actions()
actions.add_action(admin)


@app.route('/v1/events/<int:id>', methods=["GET"])
def get_by_id(id):
    res = actions.get_action_by_id(id)
    if res == 'not fund':
        return res, 404
    return res, 200


@app.route('/v1/events/', methods=["GET"])
def get_list_from_to():
    parser = reqparse.RequestParser()
    parser.add_argument("start_time")
    parser.add_argument("end_time")
    args = parser.parse_args()
    start_time = DateTime(args["start_time"])
    end_time = DateTime(args["end_time"])
    return jsonify(start_time=str(start_time), end_time=str(end_time),
                   events=[action.to_json() for action in actions.get_list_from_to(start_time, end_time)]), 200


@app.route('/v1/events/', methods=['POST'])
def add_action():
    if not request.json:
        abort(400)
    act = Action.from_json(request.json)
    actions.add_action(act)
    return act.to_json(), 200


@app.route('/v1/events/<int:id>', methods=['DELETE'])
def del_action(id):
    res = actions.del_action_by_id(id)
    if res == "Can`t be deleted":
        return res, 500
    elif res == "{} is not in list.".format(id):
        return res, 404
    return res, 200


app.run(debug=True)
