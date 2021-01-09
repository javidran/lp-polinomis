from ConvexPolygon import ConvexPolygon
if __name__ is not None and "." in __name__:
    from .PolygonParser import PolygonParser
    from .PolygonVisitor import PolygonVisitor
else:
    from PolygonParser import PolygonParser
    from PolygonVisitor import PolygonVisitor


# This class defines a complete generic visitor for a parse tree produced by PolygonParser.

class PolygonVisitorEval(PolygonVisitor):
    polygons = {}

    def visitString(self, ctx: PolygonParser.StringContext):
        return ctx.getChild(1)

    def visitPoint(self, ctx: PolygonParser.PointContext):
        return float(ctx.getChild(0)), float(ctx.getChild(1))

    def visitRandom(self, ctx: PolygonParser.RandomContext):
        return ConvexPolygon.random(int(ctx.getChild(1)))

    def visitNewpolygon(self, ctx: PolygonParser.NewpolygonContext):
        point_list = []
        for i in range(1, ctx.getChildCount() - 2):
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
        return self.visit(ctx.getChild(0))

    def visitPriority(self, ctx: PolygonParser.PriorityContext):
        return self.visit(ctx.getChild(1))

    def visitAssig(self, ctx: PolygonParser.AssigContext):
        polygon = self.visit(ctx.getChild(2))
        self.polygons[ctx.getChild(0)] = polygon

    def visitAssignedid(self, ctx: PolygonParser.AssignedidContext):
        return self.polygons[ctx.getChild(0)]

    def visitPrintsmth(self, ctx:PolygonParser.PrintsmthContext):
        print(self.visit(ctx.getChild(1)))

    def visitArea(self, ctx: PolygonParser.AreaContext):
        polygon = self.visit(ctx.getChild(1))
        print(polygon.get_area())

    def visitPerimeter(self, ctx: PolygonParser.PerimeterContext):
        polygon = self.visit(ctx.getChild(1))
        print(polygon.get_perimeter())

    def visitVertices(self, ctx: PolygonParser.VerticesContext):
        polygon = self.visit(ctx.getChild(1))
        print(polygon.number_of_vertices())

    def visitCentroid(self, ctx: PolygonParser.CentroidContext):
        polygon = self.visit(ctx.getChild(1))
        print(polygon.get_centroid())

    def visitInside(self, ctx: PolygonParser.InsideContext):
        a = self.visit(ctx.getChild(1))
        b = self.visit(ctx.getChild(2))
        print("yes") if a.contains_convex_polygon(b) else print("no")

    def visitEqual(self, ctx: PolygonParser.EqualContext):
        a = self.visit(ctx.getChild(1))
        b = self.visit(ctx.getChild(2))
        print("yes") if a == b else print("no")

    def visitColornum(self, ctx:PolygonParser.ColornumContext):
        return float(ctx.getChild(0)), float(ctx.getChild(1)), float(ctx.getChild(2))

