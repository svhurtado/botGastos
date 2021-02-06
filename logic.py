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