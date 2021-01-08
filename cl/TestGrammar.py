import sys
from antlr4 import *
from PolygonLexer import PolygonLexer
from PolygonParser import PolygonParser
from PolygonVisitor import PolygonVisitor

input_stream = FileStream("script.txt")
lexer = PolygonLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = PolygonParser(token_stream)
tree = parser.root()

visitor = PolygonVisitor()
visitor.visit(tree)
