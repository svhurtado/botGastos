import database.db as db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Account(db.Base):
    """La cuenta de una persona, que abarca ingresos y gastos """
    
    __tablename__ = 'accounts'   #Asociar con la tabla en la BD
    
    #Definición de las columnas y relaciones
    id = Column('id', String(15), primary_key=True, nullable=False)
    balance = Column('balance', Float, server_default='0', nullable=False)
    earnings = relationship('Earning', back_populates='accounts')
    spendings = relationship('Spending', back_populates='accounts')

    #Constructor
    def __init__(self, id, balance=0):
        self.id = id
        self.balance = balance
    
    #Es como el "toString"
    def __repr__(self):
        return f"<Account {self.id}>"