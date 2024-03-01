from flask import Flask, render_template
from sqlalchemy.orm import Session

from src.blueprints.error_blueprint import error_blueprint
from src.blueprints.create_blueprint import create_blueprint
from src.blueprints.statistics_blueprint import statistics_blueprint

from src.db_config import main_page_view, database

app = Flask(__name__)
app.register_blueprint(error_blueprint)
app.register_blueprint(create_blueprint)
app.register_blueprint(statistics_blueprint)

@app.template_filter()
def format_date_to_german(value):
    return value.strftime('%d.%m.%Y')


@app.route('/')
def index():
    with Session(database) as sess:
        result = sess.execute(main_page_view.select())
        spiele = [list(res._asdict().values()) for res in result]
        gelbe = 0
        gelb_rote = 0
        rote = 0
    for spiel in spiele:
        gelbe += spiel[6]
        gelbe += spiel[9]
        gelb_rote += spiel[8]
        gelb_rote += spiel[11]
        rote += spiel[7]
        rote += spiel[10]
    return render_template('base.html', spiele=spiele, gelbe=gelbe, gelb_rote=gelb_rote, rote=rote)

if __name__ == '__main__':
    app.run(port=5003)  
