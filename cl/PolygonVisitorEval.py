if __name__ is not None and "." in __name__:
    from .PolygonParser import PolygonParser
    from .PolygonVisitor import PolygonVisitor
else:
    from PolygonParser import PolygonParser
    from PolygonVisitor import PolygonVisitor


# This class defines a complete generic visitor for a parse tree produced by PolygonParser.

class PolygonVisitorEval(PolygonVisitor):

    def visitString(self, ctx: PolygonParser.StringContext):
        return ctx.getChild(1).getText()

    def visitPrintstring(self, ctx: PolygonParser.PrintstringContext):
        print(self.visit(ctx.getChild(1)))
