"""Return JSON representations of codebook data."""

from flask import Blueprint, jsonify, request
import pickle


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix='/api')


db = pickle.load(file('codebook/db.pck', 'rb'))


@index_blueprint.route('/codebook/', methods=['GET'])
def get_all_codebook_data():
    """Return all codebook data
    """
    if 'q' in request.args:
        q = request.args.get('q')
        results = _search_description_by_query(q)
    else:
        results = [_prepare_data(code, data) for code, data in db.items()]
    return jsonify(results)


@index_blueprint.route('/codebook/<string:code>', methods=['GET'])
def get_specific_codebook_data(code):
    """Return codebook data for associated code.
    """
    try:
        data = db[code]
    except KeyError:
        return jsonify({
            'status': 'error',
            'message': 'Invalid codename.'
        })
    return jsonify(_prepare_data(code, data))


def _prepare_data(code, data):
    """Format data for API.
    """
    results = {
        'code': code,
        'description': data['description']
    }
    results.update(_add_metadata(data))
    return results


def _add_metadata(data):
    """Builds question metadata based on specified fields.
    """
    keys = ['type', 'label', 'range', 'units', 'unique values', 'missing',
            'source file']
    results = {}
    for key, val in data.items():
        if key in keys:
            results[key] = val
    return results


def _search_description_by_query(q):
    """Returns questions whose description contains the query.
    """
    results = []
    for code, data in db.items():
        if q in data['description']:
            results.append(_prepare_data(code, data))
    return results