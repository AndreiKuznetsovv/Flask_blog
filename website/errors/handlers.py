from flask import render_template, Blueprint
from werkzeug.exceptions import NotFound, InternalServerError, Forbidden

errors = Blueprint('errors', __name__)


# error handler for 404
@errors.app_errorhandler(NotFound)
def page_not_found(e):
    return render_template('errors/error_404.html'), 404


# error handler for 500
@errors.app_errorhandler(InternalServerError)
def internal_server_error(e):
    return render_template('errors/error_500.html'), 500


# error handler for 403
@errors.app_errorhandler(Forbidden)
def forbidden_error(e):
    return render_template('errors/error_403.html'), 403
