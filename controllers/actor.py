from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()

    for field in ACTOR_FIELDS[1:]:
        if field not in data.keys():
            err = f"{field} missing in data"
            return make_response(jsonify(error=err), 400)

    for key in data.keys():
        if key not in ACTOR_FIELDS[1:]:
            err = f"{key} is not a required field"
            return make_response(jsonify(error=err), 400)

    # Check if data_of_birth is in format DATE_FORMAT
    try:
        data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT)
    except:
        err = "Date of birth format error"
        return make_response(jsonify(error=err), 400)

    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}

    return make_response(jsonify(new_actor), 200)


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()

    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    for key in data.keys():
        if key not in ACTOR_FIELDS:
            err = f"{key} is not a required field"
            return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data['id'])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    # Check if data_of_birth is in format DATE_FORMAT
    if 'date_of_birth' in data.keys():
        try:
            data['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT)
        except:
            err = "Date of birth format error"
            return make_response(jsonify(error=err), 400)

    obj = Actor.query.filter_by(id=row_id).first()
    if obj is None:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    upd_record = Actor.update(row_id, **data)
    upd_actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data['id'])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    obj = Actor.query.filter_by(id=row_id).first()
    if obj is None:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    del_act = Actor.delete(data['id'])
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    if not all(key in data for key in ['id', 'relation_id']):
        err = 'Bad request: id and relation_id fields are required'
        return make_response(jsonify(error=err), 400)

    try:
        data['id'] = int(data['id'])
        data['relation_id'] = int(data['relation_id'])
    except:
        err = 'Id and relation_id must be integer'
        return make_response(jsonify(error=err), 400)

    actor = Actor.query.get(data['id'])
    if not actor:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    movie = Movie.query.get(data['relation_id'])
    if not movie:
        err = 'Movie with such id does not exist'
        return make_response(jsonify(error=err), 400)

    actor = Actor.add_relation(data['id'], movie)# add relation here
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)

# def actor_clear_relations():
#     """
#     Clear all relations by id
#     """
#     data = get_request_data()
#     print(data, '-_-_-')
#     if not all(key in data for key in ['id', 'relation_id']):
#         err = 'Bad request: id and relation_id fields are required'
#         return make_response(jsonify(error=err), 400)
#
#     try:
#         data['id'] = int(data['id'])
#         data['relation_id'] = int(data['relation_id'])
#     except:
#         err = 'Id and relation_id must be integer'
#         return make_response(jsonify(error=err), 400)
#
#     actor = Actor.query.get(data['id'])
#     if not actor:
#         err = 'Record with such id does not exist'
#         return make_response(jsonify(error=err), 400)
#
#     movie = Movie.query.get(data['relation_id'])
#     if not movie:
#         err = 'Movie with such id does not exist'
#         return make_response(jsonify(error=err), 400)
#
#     # use this for 200 response code
#     actor = Actor.remove_relation(data['id'], movie)   # clear relations here
#     rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
#     rel_actor['filmography'] = str(actor.filmography)
#     return make_response(jsonify(rel_actor), 200)

def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    print(data, '-_-_-')
    if 'id' not in data.keys():
        err = 'id field is required'
        return make_response(jsonify(error=err), 400)

    try:
        data['id'] = int(data['id'])
    except:
        err = 'Id and relation_id must be integer'
        return make_response(jsonify(error=err), 400)

    actor = Actor.query.get(data['id'])
    if not actor:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)


    # use this for 200 response code
    actor = Actor.clear_relations(data['id'])   # clear relations here
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)
