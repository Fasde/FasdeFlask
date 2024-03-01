from flask import Blueprint, request, render_template, redirect
from sqlalchemy.orm import Session
from uuid import uuid4
import json

from ..db_config import spiele_table, team_table, tor_table, karte_table, strafstoss_table, database
from ..util import UUIDEncoder

create_blueprint = Blueprint('create', __name__, url_prefix='/create')


@create_blueprint.route('/spiel', methods=['GET', 'POST'])
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
        return render_template('create/spiel.html', teams=teams, ligen=ligen, orte=orte, success=success)
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
    return redirect('/create/spiel?success=True')

@create_blueprint.route('/team', methods=['GET', 'POST'])
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
        return render_template('create/team.html', teams=teams, success=success)
    verein = request.form.get('verein', type=str)
    mannschaft = request.form.get('mannschaft', type=str)
    insert = team_table.insert()
    insert = insert.values(team_id=uuid4(),verein=verein,mannschaft=mannschaft)
    with Session(database) as sess:
        sess.execute(insert)
        sess.commit()
    return redirect('/create/team?success=True')

@create_blueprint.route('/tor', methods=['GET', 'POST'])
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
        return render_template('create/tor.html', teams=teams, spiele=spiele, teamsjson=json.dumps(teams, cls=UUIDEncoder), success=success)
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
    return redirect('/create/tor?success=True')

@create_blueprint.route('/karte', methods=['GET', 'POST'])
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
        return render_template('create/karte.html', teams=teams, spiele=spiele, teamsjson=json.dumps(teams, cls=UUIDEncoder), success=success)
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
    return redirect('/create/karte?success=True')

@create_blueprint.route('/strafstoss', methods=['GET', 'POST'])
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
        return render_template('create/strafstoss.html', teams=teams, spiele=spiele, teamsjson=json.dumps(teams, cls=UUIDEncoder), success=success)
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
    return redirect('/create/strafstoss?success=True')

