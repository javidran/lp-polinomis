# Generated from Polygon.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PolygonParser import PolygonParser
else:
    from PolygonParser import PolygonParser

# This class defines a complete generic visitor for a parse tree produced by PolygonParser.

class PolygonVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PolygonParser#root.
    def visitRoot(self, ctx:PolygonParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#string.
    def visitString(self, ctx:PolygonParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#point.
    def visitPoint(self, ctx:PolygonParser.PointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#random.
    def visitRandom(self, ctx:PolygonParser.RandomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#newpolygon.
    def visitNewpolygon(self, ctx:PolygonParser.NewpolygonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#convexunion.
    def visitConvexunion(self, ctx:PolygonParser.ConvexunionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#intersection.
    def visitIntersection(self, ctx:PolygonParser.IntersectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#polygonid.
    def visitPolygonid(self, ctx:PolygonParser.PolygonidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#priority.
    def visitPriority(self, ctx:PolygonParser.PriorityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#bounding.
    def visitBounding(self, ctx:PolygonParser.BoundingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#assig.
    def visitAssig(self, ctx:PolygonParser.AssigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#printsmth.
    def visitPrintsmth(self, ctx:PolygonParser.PrintsmthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#area.
    def visitArea(self, ctx:PolygonParser.AreaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#perimeter.
    def visitPerimeter(self, ctx:PolygonParser.PerimeterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#vertices.
    def visitVertices(self, ctx:PolygonParser.VerticesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#centroid.
    def visitCentroid(self, ctx:PolygonParser.CentroidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#inside.
    def visitInside(self, ctx:PolygonParser.InsideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#equal.
    def visitEqual(self, ctx:PolygonParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#draw.
    def visitDraw(self, ctx:PolygonParser.DrawContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#colornum.
    def visitColornum(self, ctx:PolygonParser.ColornumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolygonParser#color.
    def visitColor(self, ctx:PolygonParser.ColorContext):
        return self.visitChildren(ctx)



del PolygonParser