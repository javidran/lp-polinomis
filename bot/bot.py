from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from antlr4 import *

try:
    from ..cl.PolygonLexer import PolygonLexer
    from ..cl.PolygonParser import PolygonParser
    from ..cl.PolygonVisitorEval import PolygonVisitorEval
except (ValueError, ImportError) as _:
    import sys
    sys.path.append("..")
    from cl.PolygonLexer import PolygonLexer
    from cl.PolygonParser import PolygonParser
    from cl.PolygonVisitorEval import PolygonVisitorEval


# Diccionario para trabajar con instancias de PolygonVisitorEval únicas por usuario.
context_visitors = {}


# Inicializador del bot para cada usuario.
def start(update, context):
    global context_visitors

    def image_handler(filename, image):
        """
        Envia la imagen recibida en formato io.BytesIO

        :param filename: Nombre de la imagen
        :param image: Imagen en instancia io.BytesIO
        """
        context.bot.send_photo(chat_id=update.effective_chat.id, caption=filename, photo=image)

    context_visitors[update.message.chat.id] = PolygonVisitorEval(image_handler)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hola! Sóc el bot d'en Javier Cabrera per la pràctica de LP Polinomis.")


# Procesador de cualquier mensaje recibido. Interpretado por el lenguaje de programación creado.
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


TOKEN = open('token.txt').read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

command_handler = CommandHandler('start', start)
dispatcher.add_handler(command_handler)
message_handler = MessageHandler(Filters.text & (~Filters.command), message)
dispatcher.add_handler(message_handler)

# Enciende el bot
updater.start_polling()
