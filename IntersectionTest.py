from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(0, 0), (0, 1), (1, 1), (0.2, 0.8)]
pointlist_2 = [(0, 0), (1, 0), (1, 1)]
cp = ConvexPolygon(pointlist)
cp2 = ConvexPolygon(pointlist_2)

cp3 = cp.intersect(cp2)
print(cp3)
cp3.draw_polygon("intersect.png")
