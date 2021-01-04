from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(0, 0), (50, 0), (50, 50), (0, 50)]
cp = ConvexPolygon(pointlist)
print("First area: " + str(cp.get_area()))

pointlist = [(0, 0), (300, 0), (250, 100), (50, 100)]
cp = ConvexPolygon(pointlist)
print("Second area: " + str(cp.get_area()))

pointlist = [(50, 100), (200, 0), (0, 0), (200, 0), (130, 200), (160, 150), (100, 0), (50, 10)]
cp = ConvexPolygon(pointlist)
print("Third area: " + str(cp.get_area()))

pointlist = [(0, 0), (0, 1), (1, 1), (0.2, 0.8)]
cp = ConvexPolygon(pointlist)
print("Fourth area: " + str(cp.get_area()))


