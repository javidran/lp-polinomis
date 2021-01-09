from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(0, 0), (300, 0), (250, 100), (50, 100)]
pointlist_2 = [(0, 0), (300, 0), (250, 50), (50, 50)]
cp = ConvexPolygon(pointlist)
cp2 = ConvexPolygon(pointlist_2)

print(cp.contains_convex_polygon(cp2))
cp.draw_polygon("prueba.png")
