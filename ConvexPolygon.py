import math
from PIL import Image, ImageDraw, ImagePath
from functools import cmp_to_key

class ConvexPolygon:
    points = None

    def __init__(self, points):
        self.points = self.__convex_hull( list(dict.fromkeys(points)) )

    def __str__(self):
        return str(self.points)

    def check_is_inside(self, point):
        pass

    def number_of_vertices(self):
        return len(self.points)

    def number_of_edges(self):
        vertices = self.number_of_vertices()
        if vertices == 1: 
            return 0
        elif vertices == 2: 
            return 1
        else: 
            return vertices

    def perimeter(self):
        sum = 0
        for dist in self.__distance_list():
            sum += dist
        return sum  

    def is_regular(self):
        dist_list = self.__distance_list()
        if self.number_of_edges() < 3: return False
        for dist in dist_list:
            if dist != dist_list[0]: return False
        return True
    
    def get_bounding_box(self):
        xmin = self.points[0][0]
        ymin = self.points[0][1]
        xmax = self.points[0][0]
        ymax = self.points[0][1]

        for point in self.points:
            if point[0] < xmin: xmin = point[0]
            if point[0] > xmax: xmax = point[0]
            if point[1] < ymin: ymin = point[1]
            if point[1] > ymax: ymax = point[1]
            
        return [(xmin, ymin), (xmax, ymax)]

    def draw_polygon(self):
        img_resolution = []
        bounding_box = self.get_bounding_box()
        img_resolution.append(bounding_box[1][0] - bounding_box[0][0])
        img_resolution.append(bounding_box[1][1] - bounding_box[0][1])

        img = Image.new("RGB", img_resolution, "white")
        imgDraw = ImageDraw.Draw(img)
        imgDraw.polygon(self.points, fill ="#ffff33", outline="blue")
        img.save("nameImage.png")

    def __calc_distance(self, point_a, point_b):
        return math.sqrt( ((point_a[0]-point_b[0])**2)+((point_a[1]-point_b[1])**2) )

    def __distance_list(self):
        if self.number_of_edges == 0: 
            return [ ]
        if self.number_of_edges == 1:
            return [ self.__calc_distance(self.points[0], self.points[1]) ]
        else :
            edge_list = [ ]
            for i in range(self.number_of_vertices()):
                if i == self.number_of_vertices()-1:
                    edge_list.append(self.__calc_distance(self.points[i], self.points[0]))
                else:
                    edge_list.append(self.__calc_distance(self.points[i], self.points[i+1]))
            return edge_list

    # To find orientation of ordered triplet (p, q, r). 
    # The function returns following values 
    # 0 --> p, q and r are colinear 
    # 1 --> Clockwise 
    # 2 --> Counterclockwise 
    def __orientation(self, pa, pb, pc):
        value = (pb[1] - pa[1]) * (pc[0] - pb[0]) - (pb[0] - pa[0]) * (pc[1] - pb[1])
        if value == 0: return 0 # Colinear
        elif value > 0: return 1 # Clockwise
        else: return 2 # Counterclockwise

    def __compare(self, point0, point1, point2):
        o = self.__orientation(point0, point1, point2)
        if o == 0:
            if self.__calc_distance(point0, point2) >= self.__calc_distance(point0, point1): 
                return -1
            else: 
                return 1
        elif o == 2: 
            return -1
        else: 
            return 1

    def __convex_hull(self, points):
        # Find the bottom-most point
        ymin = points[0][1]
        min = 0
        for i, point in enumerate(points):
            y = point[1]
            if y < ymin or (y == ymin and point[0] < points[min][0]):
                ymin = y
                min = i

        # Place the bottom-most point at first position
        tmp = points[0]
        points[0] = points[min]
        points[min] = tmp

        #Order points in counterclockwise
        points = [points[0]] + sorted(points[1:], key=cmp_to_key(lambda x,y:self.__compare(points[0], x, y)))

        # If two or more points are colinear, we will remove all the points in the middle
        # The compare function puts the farthest point at the end
        points_without_colinear = []
        for i in range(len(points)):
            if i > 0 and i < len(points)-1 and self.__orientation(points[0], points[i], points[i+1]) == 0:
                continue
            points_without_colinear.append(points[i])

        points = points_without_colinear

        # If we have less than 3 vertices, we don't need to do more calculus.
        if len(points) < 3: return points

        # Create an empty stack with the 3 first points
        stack  = []
        for p in points[:3]:
            stack.append(p)

        # Iterate every vertex to check if it can form part of the convex hull.
        for i in range(3, len(points)):
            while self.__orientation(stack[len(stack)-2], stack[len(stack)-1], points[i]) != 2:
                stack.pop()
            stack.append(points[i])
        
        return stack