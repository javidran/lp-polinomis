# importa l'API de Telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from antlr4 import *
from cl.PolygonLexer import PolygonLexer
from cl.PolygonParser import PolygonParser
from cl.PolygonVisitorEval import PolygonVisitorEval


# Inicialitzador del bot per a un usuari.
def start(update, context):
    context_visitors[context] = PolygonVisitorEval()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hola! Sóc el bot d'en Javier Cabrera per la pràctica de LP Polinomis.")

# Processament de missatge rebut
def message(update, context):
    input_stream = InputStream(update.message.text)
    lexer = PolygonLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PolygonParser(token_stream)
    tree = parser.root()

    context_visitors[context].visit(tree)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

context_visitors = {}

# indica que quan el bot rebi la comanda /start s'executi la funció start
command_handler = CommandHandler('start', start)
dispatcher.add_handler(command_handler)
message_handler = MessageHandler(Filters.text & (~Filters.command), message)
dispatcher.add_handler(message_handler)

# engega el bot
updater.start_polling()
