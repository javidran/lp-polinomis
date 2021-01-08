from antlr4 import *
from PolygonLexer import PolygonLexer
from PolygonParser import PolygonParser
from PolygonVisitorEval import PolygonVisitorEval

input_stream = InputStream(input('? '))
lexer = PolygonLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PolygonParser(token_stream)
tree = parser.root()

visitor = PolygonVisitorEval()
visitor.visit(tree)
