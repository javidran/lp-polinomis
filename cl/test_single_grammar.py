from antlr4 import *
from PolygonLexer import PolygonLexer
from PolygonParser import PolygonParser
from PolygonVisitorEval import PolygonVisitorEval

# Script que permite enviar un comando al lenguaja de programación definido por la gramatica Polygon

input_stream = InputStream(input('? '))
lexer = PolygonLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PolygonParser(token_stream)
tree = parser.root()

visitor = PolygonVisitorEval()
print(visitor.visit(tree))
