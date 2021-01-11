from ConvexPolygon import ConvexPolygon

if __name__ is not None and "." in __name__:
    from .PolygonParser import PolygonParser
    from .PolygonVisitor import PolygonVisitor
else:
    from PolygonParser import PolygonParser
    from PolygonVisitor import PolygonVisitor


# This class defines a complete generic visitor for a parse tree produced by PolygonParser.

class PolygonVisitorEval(PolygonVisitor):

    def __init__(self, image_handler=None):
        self.polygons = {}
        self.image_handler = image_handler

    def visitRoot(self, ctx: PolygonParser.RootContext):
        output = ""
        for i in range(ctx.getChildCount()):
            result = self.visit(ctx.getChild(i))
            if isinstance(result, str):
                output += result
        return output

    def visitString(self, ctx: PolygonParser.StringContext):
        return ctx.getChild(1).getText()

    def visitPoint(self, ctx: PolygonParser.PointContext):
        return float(ctx.getChild(0).getText()), float(ctx.getChild(1).getText())

    def visitRandom(self, ctx: PolygonParser.RandomContext):
        return ConvexPolygon.random(int(ctx.getChild(1).getText()))

    def visitNewpolygon(self, ctx: PolygonParser.NewpolygonContext):
        point_list = []
        for i in range(1, ctx.getChildCount() - 1):
            point_list.append(self.visit(ctx.getChild(i)))
        return ConvexPolygon(point_list)

    def visitConvexunion(self, ctx: PolygonParser.ConvexunionContext):
        a = self.visit(ctx.getChild(0))
        b = self.visit(ctx.getChild(2))
        return a.union(b)

    def visitIntersection(self, ctx: PolygonParser.IntersectionContext):
        a = self.visit(ctx.getChild(0))
        b = self.visit(ctx.getChild(2))
        return a.intersect(b)

    def visitPolygonid(self, ctx: PolygonParser.PolygonidContext):
        id = ctx.getChild(0).getText()
        return self.polygons[id]

    def visitPriority(self, ctx: PolygonParser.PriorityContext):
        return self.visit(ctx.getChild(1))

    def visitAssig(self, ctx: PolygonParser.AssigContext):
        polygon = self.visit(ctx.getChild(2))
        self.polygons[ctx.getChild(0).getText()] = polygon

    def visitPrintsmth(self, ctx: PolygonParser.PrintsmthContext):
        return str(self.visit(ctx.getChild(1))) + "\n"

    def visitBounding(self, ctx: PolygonParser.BoundingContext):
        polygon = self.visit(ctx.getChild(1))
        return ConvexPolygon(polygon.get_bounding_box())

    def visitArea(self, ctx: PolygonParser.AreaContext):
        polygon = self.visit(ctx.getChild(1))
        return str(format(polygon.get_area(), ".3f")) + "\n"

    def visitPerimeter(self, ctx: PolygonParser.PerimeterContext):
        polygon = self.visit(ctx.getChild(1))
        return str(format(polygon.get_perimeter(), ".3f")) + "\n"

    def visitVertices(self, ctx: PolygonParser.VerticesContext):
        polygon = self.visit(ctx.getChild(1))
        return str(polygon.number_of_vertices()) + "\n"

    def visitCentroid(self, ctx: PolygonParser.CentroidContext):
        polygon = self.visit(ctx.getChild(1))
        centroid = polygon.get_centroid()
        return str(format(centroid[0], ".3f") + " " + format(centroid[0], ".3f")) + "\n"

    def visitInsidepoint(self, ctx: PolygonParser.InsideContext):
        a = self.visit(ctx.getChild(2))
        b = self.visit(ctx.getChild(5))
        answer = ("yes" if b.contains_point(a) else "no")
        return answer + "\n"

    def visitInsidepolygon(self, ctx: PolygonParser.InsideContext):
        a = self.visit(ctx.getChild(1))
        b = self.visit(ctx.getChild(3))
        answer = ("yes" if a.contains_convex_polygon(b) else "no")
        return answer + "\n"

    def visitEqual(self, ctx: PolygonParser.EqualContext):
        a = self.visit(ctx.getChild(1))
        b = self.visit(ctx.getChild(3))
        answer = ("yes" if a == b else"no")
        return answer + "\n"

    def visitDraw(self, ctx: PolygonParser.DrawContext):
        filename = self.visit(ctx.getChild(1))
        polygon_list = []
        for i in range(3, ctx.getChildCount(), 2):
            polygon_list.append(self.visit(ctx.getChild(i)))
        ConvexPolygon.draw(filename, polygon_list, self.image_handler)

    def visitColornum(self, ctx: PolygonParser.ColornumContext):
        return float(ctx.getChild(0).getText()), float(ctx.getChild(1).getText()), float(ctx.getChild(2).getText())

    def visitColor(self, ctx: PolygonParser.ColorContext):
        polygon = self.visit(ctx.getChild(1))
        color = self.visit(ctx.getChild(4))
        polygon.set_color(color)
