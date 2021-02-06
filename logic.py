""" La lógica del negocio """
import database.db as db
from models.Account import Account
from models.Earning import Earning
from models.Spending import Spending
from datetime import datetime
from sqlalchemy import extract

#Mensaje del About
def get_about_this(VERSION):
    response = (
        f"Simple Expenses Bot (pyTelegramBot) v{VERSION}"
        "\n\n"
        "Desarrollado por Jorge I. Meza <jimezam@autonoma.edu.co>")
    return response

#Mensaje de ayuda, con los comandos y mensajes
def get_help_message ():
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot (obligatorio)\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*/about* - Muestra detalles de esta aplicación\n"
        "*gane|gané|g {cantidad}* - Registra un saldo positivo\n"
        "*gaste|gasté|gg {cantidad}* - Registra un saldo negativo\n"
        "*listar ganancias|lg en {índice_mes} de {año}* - Lista las ganancias de un mes/año\n"
        "*listar gastos|lgg en {mes} de {año}* - Lista los gastos de un mes/año\n"
        "*obtener saldo|s* - Muestra el saldo actual (disponible)\n"
        "*remover|r ganancia|g|gasto|gg {índice}* - Remueve una ganancia o un gasto según su índice\n"
        "*listar cuentas|lc* - Lista las cuentas registradas (sólo admin)\n")
    return response

#Mensaje de bienvenida
def get_welcome_message(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* "
        f"también conocido como *{bot_data.username}*.\n\n"
        "¡Estoy aquí para ayudarte a registrar tus gastos!")
    return response

#Registrar un usuario
def register_account(user_id):
    #Consulta por llave primaria
    account = db.session.query(Account).get(user_id)
    db.session.commit() #Es posible que esto no sea necesario con otro motor de BD, pero en SQLite evita problemas de hilos
    
    if account == None:
        account = Account(user_id, 0)
        db.session.add(account)
        db.session.commit()
        return True
    
    return False

#Consultar el saldo
def get_balance (user_id):
    account = db.session.query(Account).get(user_id)
    db.session.commit()

    if not account:
        return None
    
    return account.balance

#Actualizar el saldo en la cuenta
def update_account (user_id, amount):
    account = db.session.query(Account).get(user_id)
    db.session.commit()

    if not account:
        return False

    account.balance = account.balance + amount
    db.session.commit()
    return True

#Registrar un ingreso
def earn_money (user_id, amount):
    if amount <= 0:
        return False

    control = update_account (user_id, amount)
    if not control:
        return False

    earn = Earning(amount,
                   datetime.now(),
                   user_id)
    db.session.add(earn)
    db.session.commit()
    return True

#Registar un gasto
def spend_money(user_id, amount):
    if amount <= 0:
        return False

    control = update_account(user_id, amount * -1)
    if not control:
        return False

    spend = Spending(amount,
                     datetime.now(),
                     user_id)
    db.session.add(spend)
    db.session.commit()
    return True

#Obtener la lista de ingresos
def list_earnings (user_id, month, year):
    earningsUsuario = db.session.query(Earning).filter_by(accounts_id=user_id)
    #Earning.when es el campo de la fecha, al cual se le saca el mes para compararlo y filtrar
    earnings = earningsUsuario.filter(extract('month', Earning.when) == month
                                      ).filter(extract('year', Earning.when) == year).all()
    db.session.commit()
    return earnings

#Obtener la lista de gastos
def list_spendings (user_id, month, year):
    spendings = db.session.query(Spending
            ).filter_by(
                accounts_id=user_id
            ).filter(
                extract('month', Spending.when) == month
            ).filter(
                extract('year', Spending.when) == year
            ).all()
            
    db.session.commit()
    return spendings

#Validar mes y año
def validate_date(month, year):
    if month < 1 or month > 12:
        return f"Error, mes inválido: {month}"

    if year < 1990 or year > 2050:
        return f"Error, año inválido: {year}"
    
    return None