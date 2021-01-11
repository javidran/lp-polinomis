from polygons import ConvexPolygon

print("Welcome to ConvexPolygon test")

pointlist = [(0, 0), (0, 1), (1, 0)]
pointlist_2 = [(0, 0), (1, 0), (1, 0.5), (0, 0.5)]
cp = ConvexPolygon(pointlist)
cp2 = ConvexPolygon(pointlist_2)

cp3 = cp.union(cp2)
print(cp3)
cp3.draw_polygon("union.png")
