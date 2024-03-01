from sqlalchemy.orm import Session
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import date
from .db_config import spiele_table, team_table, tor_table, karte_table, strafstoss_table, main_page_view, database

def spiele_pro_monat(von, bis):
    with Session(database) as sess:
        result = sess.execute(spiele_table.select().where(spiele_table.c.datum.between(von, bis)))
        spiele = [list(res._asdict().values()) for res in result]
        monate = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
        spiel_daten = {}
        for spiel in spiele:
            datum: date = spiel[6]
            year = datum.year
            month = datum.month
            if year not in spiel_daten.keys():
                spiel_daten[year] = [0,0,0,0,0,0,0,0,0,0,0,0]
            spiel_daten[year][month-1] += 1
        summiert = [0,0,0,0,0,0,0,0,0,0,0,0]
        fig = go.Figure()
        for year in spiel_daten.keys():
            for index,val in enumerate(spiel_daten[year]):
                summiert[index] += val
            fig.add_trace(go.Scatter(x=monate,y=spiel_daten[year],mode='lines+markers',name=str(year)))
        fig.add_trace(go.Scatter(x=monate,y=summiert,mode='lines+markers',name='Summiert'))
        fig.update_layout(title="Spiele pro Monat und Jahr")
        fig.update_yaxes(tickvals=list(range(max(summiert)+1)))
        return plot(fig, output_type='div')