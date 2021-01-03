from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(0,0), (0,100), (100,100), (100,0)]
cp = ConvexPolygon(pointlist)
cp.convex_hull()


cp.print_point_list()
print(pointlist)



cp.draw_polygon()
print(cp.perimeter())
print(cp.is_regular())
