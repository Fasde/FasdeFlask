from flask import render_template, Blueprint

error_blueprint = Blueprint('error_blueprint', __name__)

@error_blueprint.errorhandler(500)
def internal_error(error):
    return render_template("error_pages/500.html")

