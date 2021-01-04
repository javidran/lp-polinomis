from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(50,100), (200,0), (0,0), (200,0), (130,200), (160,150), (100,0), (50, 10)]
pointlist_2 = [(300,0), (0,0), (300,20), (0,20)]
cp = ConvexPolygon(pointlist)
cp2 = ConvexPolygon(pointlist_2)

union = cp.union(cp2)
union.draw_polygon()
