#!/usr/bin/python3
from flask import jsonify, abort, request

from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """Returns all states"""
    return jsonify([i.to_dict() for i in storage.all(State).values()])


@app_views.route('/states/<string:state_id>')
def get_state_by_id(state_id):
    """Searches and State by id"""
    state : State = storage.get(State, state_id)
    return jsonify(state.to_dict()) if state else abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_post():
    """Method that post a new state"""
    data_state = request.get_json(silent=True)

    if (type(data_state) is dict):
        new_state = State(**data_state)
        if (not new_state.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400
        new_state.save()
        return (jsonify(new_state.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id):
    """Method that delete a state by id"""
    delete_state = storage.get(State, state_id)
    if delete_state is None:
        abort(404)
    else:
        delete_state.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def states_put(state_id):
    """Method to update/put a state by id"""
    actual_state = storage.get(State, state_id)
    if (actual_state is None):
        abort(404)

    update_state = request.get_json(silent=True)
    if (type(update_state) is dict):
        update_state.pop('id', None)
        update_state.pop('created_at', None)
        update_state.pop('updated_at', None)

        for key, value in update_state.items():
            setattr(actual_state, key, value)
        actual_state.save()
        return (jsonify(actual_state.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
