from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(50, 150), (200, 50), (350, 150), (350, 300), (250, 300), (200, 250), (150, 350), (100, 250), (100, 200)]
pointlist_2 = [(100, 100), (300, 100), (300, 300), (100, 300)]
cp = ConvexPolygon(pointlist)
cp2 = ConvexPolygon(pointlist_2)

print(cp.intersect(cp2))
cp.draw_polygon()
