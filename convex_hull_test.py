from ConvexPolygon import ConvexPolygon

print("Welcome to ConvexPolygon implementation")

pointlist = [(50,100), (200,0), (0,0), (200,0), (130,200), (160,150), (100,0), (50, 10)]
cp = ConvexPolygon(pointlist)

print("")
print(pointlist)
cp.print_point_list()

cp.draw_polygon()
