from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from antlr4 import *
from cl.PolygonLexer import PolygonLexer
from cl.PolygonParser import PolygonParser
from cl.PolygonVisitorEval import PolygonVisitorEval

# Diccionari per treballar amb les instàncies de PolygonVisitorEval per a cada usuari
context_visitors = {}


# Inicialitzador del bot per a un usuari.
def start(update, context):
    global context_visitors

    def image_handler(filename, image):
        context.bot.send_photo(chat_id=update.effective_chat.id, caption=filename, photo=image)

    context_visitors[update.message.chat.id] = PolygonVisitorEval(image_handler)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hola! Sóc el bot d'en Javier Cabrera per la pràctica de LP Polinomis.")


# Processament de missatge rebut
def message(update, context):
    global context_visitors

    input_stream = InputStream(update.message.text)
    lexer = PolygonLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PolygonParser(token_stream)
    tree = parser.root()

    response = context_visitors[update.message.chat.id].visit(tree)
    if response:
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

command_handler = CommandHandler('start', start)
dispatcher.add_handler(command_handler)
message_handler = MessageHandler(Filters.text & (~Filters.command), message)
dispatcher.add_handler(message_handler)

# Engega el bot
updater.start_polling()
