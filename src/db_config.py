from sqlalchemy import Uuid, String, Date, Integer, Table, create_engine, MetaData, Column, ForeignKey, Boolean, Time

database = create_engine('postgresql+psycopg2://pi:pi@192.168.178.33:5432/spieldatenbank')
metadata = MetaData()


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