from flask import Flask

from src.blueprints.error_blueprint import error_blueprint
from src.blueprints.routes_blueprint import routes_blueprint

app = Flask(__name__)
app.register_blueprint(error_blueprint)
app.register_blueprint(routes_blueprint)

@app.template_filter()
def format_date_to_german(value):
    return value.strftime('%d.%m.%Y')

if __name__ == '__main__':
    app.run(port=5003)  
