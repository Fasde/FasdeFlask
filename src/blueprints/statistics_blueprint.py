from flask import Blueprint, request, render_template, redirect
from sqlalchemy.orm import Session
from uuid import uuid4
from ..statistics import spiele_pro_monat
from datetime import date

statistics_blueprint = Blueprint('stats', __name__, url_prefix='/statistics')


@statistics_blueprint.route('/spiel', methods=['GET', 'POST'])
def stats_spiel():
    von = request.form.get('von')
    bis = request.form.get('bis')
    if von == '':
        von = date(date.today().year, 1, 1)
    if bis == '':
        bis = date(date.today().year, 12, 31)
    spm = spiele_pro_monat(von, bis)
    return render_template('statistics/spiel.html', spm=spm)


@statistics_blueprint.route('/team', methods=['GET', 'POST'])
def stats_team():
    return render_template('statistics/team.html')


@statistics_blueprint.route('/tor', methods=['GET', 'POST'])
def stats_tor():
    return render_template('statistics/tor.html')

@statistics_blueprint.route('/karte', methods=['GET', 'POST'])
def stats_karte():
    return render_template('statistics/team.html')

@statistics_blueprint.route('/strafstoss', methods=['GET', 'POST'])
def stats_strafstoss():
    return render_template('statistics/strafstoss.html')

