import math
from PIL import Image, ImageDraw, ImagePath
from functools import cmp_to_key

class ConvexPolygon:
    points = None

    def __init__(self, points):
        self.points = list(dict.fromkeys(points)) #Con comprobar si es convexo deberia evitar hacer esto
        self.convex_hull()

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
        for dist in self.distance_list():
            sum += dist
        return sum

    def is_regular(self):
        dist_list = self.distance_list()
        if self.number_of_edges() < 3: return False
        for dist in dist_list:
            if dist != dist_list[0]: return False
        return True

    def draw_polygon(self):
        image = ImagePath.Path(self.points).getbbox()   
        size = list(map(int, map(math.ceil, image[2:]))) 

        im = Image.new("RGB", size, "white")

        img1 = ImageDraw.Draw(im)
        img1.polygon(self.points, fill ="#ffff33", outline="blue")
        im.save("nameImage.png")

    def print_point_list(self):
        print(self.points)

    def calc_distance(self, point_a, point_b):
        return math.sqrt( ((point_a[0]-point_b[0])**2)+((point_a[1]-point_b[1])**2) )

    def distance_list(self):
        if self.number_of_edges == 0: 
            return [ ]
        if self.number_of_edges == 1:
            return [ self.calc_distance(self.points[0], self.points[1]) ]
        else :
            edge_list = [ ]
            for i in range(self.number_of_vertices()):
                if i == self.number_of_vertices()-1:
                    edge_list.append(self.calc_distance(self.points[i], self.points[0]))
                else:
                    edge_list.append(self.calc_distance(self.points[i], self.points[i+1]))
            return edge_list

    # To find orientation of ordered triplet (p, q, r). 
    # The function returns following values 
    # 0 --> p, q and r are colinear 
    # 1 --> Clockwise 
    # 2 --> Counterclockwise 
    def orientation(self, pa, pb, pc):
        value = (pb[1] - pa[1]) * (pc[0] - pb[0]) - (pb[0] - pa[0]) * (pc[1] - pb[1])
        if value == 0: return 0 # Colinear
        elif value > 0: return 1 # Clockwise
        else: return 2 # Counterclockwise

    def compare(self, point1, point2):
        o = self.orientation(self.points[0], point1, point2)
        if o == 0:
            if self.calc_distance(self.points[0], point2) >= self.calc_distance(self.points[0], point1): 
                return -1
            else: 
                return 1
        elif o == 2: 
            return -1
        else: 
            return 1

    def convex_hull(self):
        # Find the bottom-most point
        ymin = self.points[0][1]
        min = 0
        for i, point in enumerate(self.points):
            y = point[1]
            if y < ymin or (y == ymin and point[0] < self.points[min][0]):
                ymin = y
                min = i

        # Place the bottom-most point at first position
        tmp = self.points[0]
        self.points[0] = self.points[min]
        self.points[min] = tmp

        #Order points in counterclockwise
        self.points = [self.points[0]] + sorted(self.points[1:], key=cmp_to_key(self.compare))

        # If two or more points are colinear, we will remove all the points in the middle
        # The compare function puts the farthest point at the end
        points_without_colinear = []

        for i in range(self.number_of_vertices()):
            if i > 0 and i < len(self.points)-1 and self.orientation(self.points[0], self.points[i], self.points[i+1]) == 0:
                continue
            points_without_colinear.append(self.points[i])

        self.points = points_without_colinear

        # If we have less than 3 vertices, we don't need to do more calculus.
        if self.number_of_vertices() < 3: return

        # Create an empty stack with the 3 first points
        stack  = []
        for p in self.points[:3]:
            stack.append(p)

        # Iterate every vertex to check if it can form part of the convex hull.
        for i in range(3, self.number_of_vertices()):
            while self.orientation(stack[len(stack)-2], stack[len(stack)-1], self.points[i]) != 2:
                stack.pop()
            stack.append(self.points[i])

        self.points = stack
        self.points.reverse()