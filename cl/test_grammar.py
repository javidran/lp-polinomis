from antlr4 import *
from PolygonLexer import PolygonLexer
from PolygonParser import PolygonParser
from PolygonVisitorEval import PolygonVisitorEval

# Script que permite comprobar la ejecución del ejemplo proporcionado en la practica de LP Polinomis

input_stream = FileStream("script.txt")
lexer = PolygonLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PolygonParser(token_stream)
tree = parser.root()

visitor = PolygonVisitorEval()
print(visitor.visit(tree))
