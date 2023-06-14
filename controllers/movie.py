from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
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

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()

    for field in MOVIE_FIELDS[1:]:
        if field not in data.keys():
            err = f"{field} is a required field"
            return make_response(jsonify(error=err), 400)

    for key in data.keys():
        if key not in MOVIE_FIELDS[1:]:
            err = f"{field} is a required field"
            return make_response(jsonify(error=err), 400)
    # Check if age is an integer
    try:
        data['year'] = int(data['year'])
    except:
        err = "Age must be an integer"
        return make_response(jsonify(error=err), 400)

    new_record = Movie.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}

    return make_response(jsonify(new_actor), 200)




def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        if not obj:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        for key in data.keys():
            if key not in MOVIE_FIELDS:
                err = 'Field must exist'
                return make_response(jsonify(error=err), 400)

        if 'year' in data.keys():
            try:
                data['year'] = int(data['year'])
            except:
                err = 'Year must be integer'
                return make_response(jsonify(error=err), 400)

        upd_record = Movie.update(row_id, **data)
        upd_movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(upd_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def delete_movie():
    """
    Delete movie by id
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

    obj = Movie.query.filter_by(id=row_id).first()
    if obj is None:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    del_act = Movie.delete(data['id'])
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)

def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    print(data, '-----*****------')
    if not all(key in data for key in ['id', 'relation_id']):
        err = 'Bad request: id and relation_id fields are required'
        return make_response(jsonify(error=err), 400)

    try:
        data['id'] = int(data['id'])
        data['relation_id'] = int(data['relation_id'])
    except:
        err = 'Id and relation_id must be integer'
        return make_response(jsonify(error=err), 400)

    movie = Movie.query.get(data['id'])
    if not movie:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    actor = Actor.query.get(data['relation_id'])
    if not actor:
        err = 'Movie with such id does not exist'
        return make_response(jsonify(error=err), 400)

    movie = Movie.add_relation(data['id'], actor)  # add relation here
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        err = 'id field is required'
        return make_response(jsonify(error=err), 400)

    try:
        data['id'] = int(data['id'])
    except:
        err = 'Id must be integer'
        print(err)
        return make_response(jsonify(error=err), 400)

    movie = Movie.query.get(data['id'])
    if not movie:
        err = 'Record with such id does not exist'
        print(err)
        return make_response(jsonify(error=err), 400)


    # use this for 200 response code
    movie = Movie.clear_relations(data['id'])  # clear relations here
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)
