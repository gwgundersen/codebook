"""Configure and start the web server."""

from flask import Flask, jsonify


app = Flask(__name__)

from codebook import endpoints
app.register_blueprint(endpoints.index_blueprint)


""" Error handling
    ------------------------------------------------------------------------"""
@app.errorhandler(404)
def page_not_found(e):
    """Handles all 404 requests.
    """
    return jsonify({
        'status': 'error',
        'message': 'Invalid API endpoint.'
    })
