if __name__ is not None and "." in __name__:
    from .PolygonParser import PolygonParser
    from .PolygonVisitor import PolygonVisitor
else:
    from PolygonParser import PolygonParser
    from PolygonVisitor import PolygonVisitor
from ConvexPolygon import ConvexPolygon


# This class defines a complete generic visitor for a parse tree produced by PolygonParser.

class PolygonVisitorEval(PolygonVisitor):

    def visitString(self, ctx: PolygonParser.StringContext):
        return ctx.getChild(1)

    def visitPoint(self, ctx: PolygonParser.PointContext):
        return float(ctx.getChild(0)), float(ctx.getChild(1))

    def visitRandom(self, ctx: PolygonParser.RandomContext):
        return ConvexPolygon.random(int(ctx.getChild(1)))

    def visitNewpolygon(self, ctx: PolygonParser.NewpolygonContext):
        point_list = []
        for i in range(1, ctx.getChildCount()-2):
            point_list.append(self.visit(ctx.getChild(i)))
        return ConvexPolygon(point_list)

    def visitConvexunion(self, ctx: PolygonParser.ConvexunionContext):

        return self.visitChildren(ctx)

    def visitPrintstring(self, ctx: PolygonParser.PrintstringContext):
        print(self.visit(ctx.getChild(1)))
