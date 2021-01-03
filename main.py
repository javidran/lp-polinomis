from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(0,0), (50,100), (200,0), (200,0), (130,200), (160,150), (100,0)]
cp = ConvexPolygon(pointlist)
cp.convex_hull()

cp.print_point_list()
print(pointlist)
cp.draw_polygon()
print(cp.perimeter())
print(cp.is_regular())
