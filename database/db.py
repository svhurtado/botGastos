from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Conexión con la BD --> la crea si no existe
# El echo en true es para que muestre mensajes, como log.
# El último parámetro se necesita en SQLite (puede que no se requiera en otras BD)
engine = create_engine (
    'sqlite:///database/accounts.sqlite',
    echo=True,
    connect_args = {'check_same_thread': False})

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()