from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(0, 0), (300, 0), (250, 100), (50, 100)]
point_1 = (150, 10)
point_2 = (310, 0)
point_3 = (200, 0)
cp = ConvexPolygon(pointlist)

print("Has to be true: " + str(cp.contains_point(point_1)))
print("Has to be false: " + str(cp.contains_point(point_2)))
print("Has to be true: " + str(cp.contains_point(point_3)))
