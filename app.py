from flask import Flask, request, render_template, redirect
from sqlalchemy.orm import Session
from sqlalchemy import Uuid, String, Date, Integer, Table, create_engine, MetaData, Column, ForeignKey, Boolean, Time
from uuid import uuid4, UUID
import json

app = Flask(__name__)
database = create_engine('postgresql+psycopg2://pi:pi@192.168.178.33:5432/spieldatenbank')
metadata = MetaData()

@app.errorhandler(500)
def internal_error(error):
    return render_template("error_pages/500.html")


@app.template_filter()
def format_date_to_german(value):
    return value.strftime('%d.%m.%Y')

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)

spiele_table = Table("spiele", metadata, 
                     Column("spiel_id", Uuid, primary_key=True),
                     Column("spielklasse", String),
                     Column("spielort", String),
                     Column("heim_fk", Uuid, ForeignKey("team.team_id")),
                     Column("gast_fk", Uuid, ForeignKey("team.team_id")),
                     Column("bemerkung", String),
                     Column("datum", Date),
                     Column("farbe_heim", String),
                     Column("farbe_gast", String),
                     Column("wetter", String),
                     Column("farbe_sr", String),
                     Column("nsz1", Integer),
                     Column("nsz2", Integer),
                     Column("uhrzeit", Time),
                     schema='spiele')

tor_table = Table("tor", metadata,
                    Column("tor_id", Uuid, primary_key=True),
                    Column("team_fk", Uuid, ForeignKey("team.team_id")),
                    Column("spielername", String),
                    Column("spielernummer", String),
                    Column("minute", Integer),
                    Column("nsz", Integer),
                    Column("art", String),
                    Column("spiel_fk", Uuid, ForeignKey("spiele.spiel_id")),
                    schema="spiele")

team_table = Table("team", metadata,
                    Column("team_id", Uuid, primary_key=True),
                    Column("verein", String),
                    Column("mannschaft", String),
                    schema="spiele")

karte_table = Table("karte", metadata,
                    Column("karte_id", Uuid, primary_key=True),
                    Column("team_fk", Uuid, ForeignKey("team.team_id")),
                    Column("spielername", String),
                    Column("spielernummer", String),
                    Column("minute", Integer),
                    Column("nsz", Integer),
                    Column("art", String),
                    Column("grund", String),
                    Column("spiel_fk", Uuid, ForeignKey("spiele.spiel_id")),
                    schema="spiele")

strafstoss_table = Table("strafstoss", metadata,
                    Column("strafstoss_id", Uuid, primary_key=True),
                    Column("team_fk", Uuid, ForeignKey("team.team_id")),
                    Column("spielername", String),
                    Column("spielernummer", String),
                    Column("minute", Integer),
                    Column("nsz", Integer),
                    Column("verwandelt_mm", Boolean),
                    Column("spiel_fk", Uuid, ForeignKey("spiele.spiel_id")),
                    schema="spiele")

main_page_view = Table("main_page_view", metadata,
                    Column("datum", Date),
                    Column("spielklasse", String),
                    Column("heim_team", String),
                    Column("gast_team", String),
                    Column("heim_tore", Integer),
                    Column("gast_tore", Integer),
                    Column("heim_gelb", Integer),
                    Column("heim_rot", Integer),
                    Column("heim_gelb_rot", Integer),
                    Column("gast_gelb", Integer),
                    Column("gast_rot", Integer),
                    Column("gast_gelb_rot", Integer),
                    schema="spiele")

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


@app.route('/anlegen/spiel', methods=['GET', 'POST'])
def insert_spiel():
    if request.method == 'GET':
        if request.args.get('success'):
            success = True
        else:
            success = False
        with Session(database) as sess:
            result = sess.execute(team_table.select())
            teams = [list(res._asdict().values()) for res in result]
            result = sess.execute(spiele_table.select())
            spiele = [list(res._asdict().values()) for res in result]
            ligen = set([spiel[1] for spiel in spiele])
            orte = set([spiel[2] for spiel in spiele])
        return render_template('spiel.html', teams=teams, ligen=ligen, orte=orte, success=success)
    spielklasse = request.form.get('spielklasse', type=str)
    spielort = request.form.get('spielort', type=str)
    heim_fk = request.form.get('heim_fk', type=str)
    gast_fk = request.form.get('gast_fk', type=str)
    bemerkung = request.form.get('bemerkung', type=str)
    datum = request.form.get('datum', type=str)
    uhrzeit = request.form.get('uhrzeit', type=str)
    farbe_heim = request.form.get('farbe_heim', type=str)
    farbe_gast = request.form.get('farbe_gast', type=str)
    wetter = request.form.get('wetter', type=str)
    farbe_sr = request.form.get('farbe_sr', type=str)
    nsz1 = request.form.get('nsz1', type=int)
    nsz2 = request.form.get('nsz2', type=int)
    insert = spiele_table.insert()
    insert = insert.values(spiel_id=uuid4(),spielklasse=spielklasse,spielort=spielort,heim_fk=heim_fk,gast_fk=gast_fk,bemerkung=bemerkung,datum=datum,farbe_heim=farbe_heim, 
                   farbe_gast=farbe_gast,wetter=wetter,farbe_sr=farbe_sr,nsz1=nsz1,nsz2=nsz2,uhrzeit=uhrzeit)
    with Session(database) as sess:
        sess.execute(insert)
        sess.commit()
    return redirect('/anlegen/spiel?success=True')

@app.route('/anlegen/team', methods=['GET', 'POST'])
def insert_team():
    if request.method == 'GET':
        if request.args.get('success'):
            success = True
        else:
            success = False
        with Session(database) as sess:
            result = sess.execute(team_table.select())
            teams = [list(res._asdict().values()) for res in result]
            teams = [team[1] for team in teams]
            teams = set(teams)
            teams = list(teams)
        return render_template('team.html', teams=teams, success=success)
    verein = request.form.get('verein', type=str)
    mannschaft = request.form.get('mannschaft', type=str)
    insert = team_table.insert()
    insert = insert.values(team_id=uuid4(),verein=verein,mannschaft=mannschaft)
    with Session(database) as sess:
        sess.execute(insert)
        sess.commit()
    return redirect('/anlegen/team?success=True')

@app.route('/anlegen/tor', methods=['GET', 'POST'])
def insert_tor():
    if request.method == 'GET':
        if request.args.get('success'):
            success = True
        else:
            success = False
        with Session(database) as sess:
            result = sess.execute(team_table.select())
            teams = [list(res._asdict().values()) for res in result]
            result = sess.execute(spiele_table.select())
            spiele = [list(res._asdict().values()) for res in result]
        return render_template('tor.html', teams=teams, spiele=spiele, teamsjson=json.dumps(teams, cls=UUIDEncoder), success=success)
    team_fk = request.form.get('team_fk', type=str)
    spielername = request.form.get('spielername', type=str)
    spielernummer = str(request.form.get('spielernummer', type=int))
    minute = request.form.get('minute', type=int)
    nsz = request.form.get('nsz', 0, type=int)
    art = request.form.get('art', type=str)
    spiel_fk = request.form.get('spiel_fk', type=str)
    insert = tor_table.insert()
    insert = insert.values(tor_id=uuid4(),team_fk=team_fk,spielername=spielername,spielernummer=spielernummer,minute=minute,nsz=nsz,art=art,spiel_fk=spiel_fk)
    with Session(database) as sess:
        sess.execute(insert)
        sess.commit()
    if art == 'Strafstoß':
        insert = strafstoss_table.insert()
        insert = insert.values(strafstoss_id=uuid4(),team_fk=team_fk,spielername=spielername,spielernummer=spielernummer,minute=minute,nsz=nsz,verwandelt_mm=True,spiel_fk=spiel_fk)
        with Session(database) as sess:
            sess.execute(insert)
            sess.commit()
    return redirect('/anlegen/tor?success=True')

@app.route('/anlegen/karte', methods=['GET', 'POST'])
def insert_karte():
    if request.method == 'GET':
        if request.args.get('success'):
            success = True
        else:
            success = False
        with Session(database) as sess:
            result = sess.execute(team_table.select())
            teams = [list(res._asdict().values()) for res in result]
            result = sess.execute(spiele_table.select())
            spiele = [list(res._asdict().values()) for res in result]
        return render_template('karte.html', teams=teams, spiele=spiele, teamsjson=json.dumps(teams, cls=UUIDEncoder), success=success)
    team_fk = request.form.get('team_fk', type=str)
    spielername = request.form.get('spielername', type=str)
    spielernummer = str(request.form.get('spielernummer', type=int))
    minute = request.form.get('minute', type=int)
    nsz = request.form.get('nsz', 0, type=int)
    art = request.form.get('art', type=str)
    grund = request.form.get('grund', type=str)
    spiel_fk = request.form.get('spiel_fk', type=str)
    insert = karte_table.insert()
    insert = insert.values(karte_id=uuid4(),team_fk=team_fk,spielername=spielername,spielernummer=spielernummer,minute=minute,nsz=nsz,art=art,grund=grund,spiel_fk=spiel_fk)
    with Session(database) as sess:
        sess.execute(insert)
        sess.commit()
    return redirect('/anlegen/karte?success=True')

@app.route('/anlegen/strafstoss', methods=['GET', 'POST'])
def insert_strafstoss():
    if request.method == 'GET':
        if request.args.get('success'):
            success = True
        else:
            success = False
        with Session(database) as sess:
            result = sess.execute(team_table.select())
            teams = [list(res._asdict().values()) for res in result]
            result = sess.execute(spiele_table.select())
            spiele = [list(res._asdict().values()) for res in result]
        return render_template('strafstoss.html', teams=teams, spiele=spiele, teamsjson=json.dumps(teams, cls=UUIDEncoder), success=success)
    team_fk = request.form.get('team_fk', type=str)
    spielername = request.form.get('spielername', type=str)
    spielernummer = str(request.form.get('spielernummer', type=int))
    minute = request.form.get('minute', type=int)
    nsz = request.form.get('nsz', 0, type=int)
    verwandelt_mm = request.form.get('verwandelt_mm', type=bool)
    spiel_fk = request.form.get('spiel_fk', type=str)
    insert = strafstoss_table.insert()
    insert = insert.values(strafstoss_id=uuid4(),team_fk=team_fk,spielername=spielername,spielernummer=spielernummer,minute=minute,nsz=nsz,verwandelt_mm=verwandelt_mm,spiel_fk=spiel_fk)
    with Session(database) as sess:
        sess.execute(insert)
        sess.commit()
    return redirect('/anlegen/strafstoss?success=True')



if __name__ == '__main__':
    app.run(port=5003, debug=True)  
