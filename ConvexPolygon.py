import math
from PIL import Image, ImageDraw
from functools import cmp_to_key
from random import random


def calc_distance(point_a, point_b):
    return math.sqrt(((point_a[0] - point_b[0]) ** 2) + ((point_a[1] - point_b[1]) ** 2))


# To find orientation of ordered triplet (p, q, r).
# The function returns following values depending of their relation
# 0 --> Collinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(pa, pb, pc):
    value = (pb[1] - pa[1]) * (pc[0] - pb[0]) - (pb[0] - pa[0]) * (pc[1] - pb[1])
    if value == 0:
        return 0  # Collinear
    elif value > 0:
        return 1  # Clockwise
    else:
        return 2  # Counterclockwise


def convex_hull(points):
    def compare(point0, point1, point2):
        o = orientation(point0, point1, point2)
        if o == 0:
            if calc_distance(point0, point2) >= calc_distance(point0, point1):
                return -1
            else:
                return 1
        elif o == 2:
            return 1
        else:
            return -1

    # Find the bottom-most point
    ymin = points[0][1]
    min_i = 0
    for i, point in enumerate(points):
        y = point[1]
        if y < ymin or (y == ymin and point[0] < points[min_i][0]):
            ymin = y
            min_i = i

    # Place the bottom-most point at first position
    tmp = points[0]
    points[0] = points[min_i]
    points[min_i] = tmp

    # Order points in clockwise
    points = [points[0]] + sorted(points[1:], key=cmp_to_key(lambda p1, p2: compare(points[0], p1, p2)))

    # If two or more points are collinear, we will remove all the points in the middle
    # The compare function puts the farthest point at the end
    points_without_collinear = []
    for i in range(len(points)):
        if 1 < i < len(points) - 1 and orientation(points[0], points[i], points[i + 1]) == 0:
            continue
        points_without_collinear.append(points[i])

    points = points_without_collinear

    # If we have less than 3 vertices, we don't need to do more calculus.
    if len(points) < 3:
        return points

    # Create an empty stack with the 3 first points
    stack = []
    for p in points[:3]:
        stack.append(p)

    # Iterate every vertex to check if it can form part of the convex hull.
    for i in range(3, len(points)):
        while len(stack) >= 2 and orientation(stack[-2], stack[-1], points[i]) != 1:
            stack.pop()
        stack.append(points[i])

    return stack


def get_square_bounding_box(bounding_box):
    xmin = bounding_box[0][0]
    ymin = bounding_box[0][1]

    # Calculate biggest distance in order to create a square box
    dist_x = bounding_box[2][0] - xmin
    dist_y = bounding_box[2][1] - ymin
    dist = (dist_x if dist_x > dist_y else dist_y)

    # Create global bounding box
    return [(xmin, ymin), (xmin, ymin + dist), (xmin + dist, ymin + dist), (xmin + dist, ymin)]


def get_draw_coordinates(square_bounding_box, point_list):
    def get_point_draw_coordinates(point):
        def get_proportion_dist(coord, initial_coord, dist):
            return float((coord - initial_coord) / dist)

        def get_img_point(coord_prop, dist, start):
            return float(coord_prop * dist + start)

        ref_dist = square_bounding_box[2][0] - square_bounding_box[0][0]
        x_proportion_dist = get_proportion_dist(point[0], square_bounding_box[0][0], ref_dist)
        y_proportion_dist = get_proportion_dist(point[1], square_bounding_box[0][1], ref_dist)

        img_max = 399
        img_min = 1
        img_dist = img_max - img_min

        x = get_img_point(x_proportion_dist, img_dist, img_min)
        y = get_img_point(y_proportion_dist, img_dist, img_min)
        return x, y

    draw_points = []
    for p in point_list:
        draw_points.append(get_point_draw_coordinates(p))

    return draw_points


class ConvexPolygon:
    points = None
    color = (59, 163, 188)

    def __init__(self, points):
        self.points = convex_hull(list(dict.fromkeys(points)))

    def __eq__(self, other):
        if isinstance(other, ConvexPolygon):
            return self.points == other.points
        return False

    def __str__(self):
        sequence = ""
        for point in self.points:
            for coord in point:
                sequence += format(coord, ".3f") + " "
        return sequence.rstrip()

    def __distance_list(self):
        if self.number_of_vertices() <= 1:
            return []
        if self.number_of_vertices() == 2:
            return [calc_distance(self.points[0], self.points[1])]
        else:
            edge_list = []
            for i in range(self.number_of_vertices()):
                if i == self.number_of_vertices() - 1:
                    edge_list.append(calc_distance(self.points[i], self.points[0]))
                else:
                    edge_list.append(calc_distance(self.points[i], self.points[i + 1]))
            return edge_list

    def get_color(self):
        return self.color

    def set_color(self, color):
        def to_int(num):
            return int(num * 255)

        self.color = tuple(map(to_int, color))

    def get_vertices(self):
        return self.points.copy()  # TODO Eliminar copy

    def number_of_vertices(self):
        return len(self.points)

    def get_perimeter(self):
        perimeter_sum = 0
        for dist in self.__distance_list():
            perimeter_sum += dist
        return round(perimeter_sum, 3)

    def is_regular(self):

        def get_angle(a, b, c):
            ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
            return ang + 360 if ang < 0 else ang

        if self.number_of_vertices() < 3:
            return False

        reference_angle = get_angle(self.points[0], self.points[1], self.points[2])
        for i in range(self.number_of_vertices()):
            if 0 < i < self.number_of_vertices() - 3 and reference_angle != get_angle(self.points[i],
                                                                                      self.points[i + 1],
                                                                                      self.points[i + 2]):
                return False
        return True

    def union(self, convex_polygon):
        unified_points = self.get_vertices() + convex_polygon.get_vertices()
        return ConvexPolygon(unified_points)

    def contains_convex_polygon(self, convex_polygon):
        unified_points = self.get_vertices() + convex_polygon.get_vertices()
        union = ConvexPolygon(unified_points)
        return union.get_vertices() == self.get_vertices()

    def intersect(self, convex_polygon):
        return self.union(convex_polygon)

        def inside(p):
            return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

        def computeIntersection():
            dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
            dp = [s[0] - e[0], s[1] - e[1]]
            n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
            n2 = s[0] * e[1] - s[1] * e[0]
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

        outputList = self.get_vertices()
        cp1 = convex_polygon.get_vertices()[0]

        for clipVertex in convex_polygon.get_vertices():
            cp2 = clipVertex
            inputList = outputList
            outputList = []
            s = inputList[0]

            for subjectVertex in inputList:
                e = subjectVertex
                if inside(e):
                    if not inside(s):
                        outputList.append(computeIntersection())
                    outputList.append(e)
                elif inside(s):
                    outputList.append(computeareaIntersection())
                s = e
            cp1 = cp2
        return (outputList)

    def contains_point(self, point):
        for i in range(self.number_of_vertices()):
            if 0 < i < self.number_of_vertices() - 1 and orientation(self.points[i], self.points[i + 1], point) == 2:
                return False
        return True

    def get_centroid(self):
        centroid_x = 0
        centroid_y = 0
        det = 0

        for i in range(self.number_of_vertices()):
            if i + 1 == self.number_of_vertices():
                j = 0
            else:
                j = i + 1

            temp_det = self.points[i][0] * self.points[j][1] - self.points[j][0] * self.points[i][1]
            det += temp_det

            centroid_x += (self.points[i][0] + self.points[j][0]) * temp_det
            centroid_y += (self.points[i][1] + self.points[j][1]) * temp_det

        centroid_x /= 3 * det
        centroid_y /= 3 * det

        return round(centroid_x, 3), round(centroid_y, 3)

    def get_area(self):
        area = 0
        j = self.number_of_vertices() - 1

        for i in range(self.number_of_vertices()):
            area += (self.points[j][0] + self.points[i][0]) * (self.points[j][1] - self.points[i][1])
            j = i

        return round(abs(area / 2.0), 3)

    def get_bounding_box(self):
        if self.number_of_vertices() == 0:
            return None

        xmin = self.points[0][0]
        ymin = self.points[0][1]
        xmax = self.points[0][0]
        ymax = self.points[0][1]

        for point in self.points:
            if point[0] < xmin:
                xmin = point[0]
            if point[0] > xmax:
                xmax = point[0]
            if point[1] < ymin:
                ymin = point[1]
            if point[1] > ymax:
                ymax = point[1]

        return [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]

    def draw_polygon(self, filename):
        b_box = get_square_bounding_box(self.get_bounding_box())

        img = Image.new("RGB", [400, 400], "white")
        img_draw = ImageDraw.Draw(img, "RGBA")
        img_draw.polygon(get_draw_coordinates(b_box, self.points), fill=self.color + (50,), outline=self.color + (255,))
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save(filename)

    @staticmethod
    def draw(filename, polygon_list):
        def create_global_box(reference_box):
            xmin = reference_box[0][0]
            ymin = reference_box[0][1]
            xmax = reference_box[2][0]
            ymax = reference_box[2][1]

            # Iterate over the other bounding boxes and get the biggest size
            for p in polygon_list[1:]:
                box = p.get_bounding_box()
                if box is None:
                    continue
                if box[0][0] < xmin:
                    xmin = box[0][0]
                if box[0][1] < ymin:
                    ymin = box[0][1]
                if box[2][0] > xmax:
                    xmax = box[2][0]
                if box[2][1] > ymax:
                    ymax = box[2][1]

            bounding_box = [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]
            return get_square_bounding_box(bounding_box)

        global_box = None

        # Search for first bounding box
        for i, polygon in enumerate(polygon_list):
            first_box = polygon.get_bounding_box()
            if first_box is not None:
                global_box = create_global_box(first_box)
                break

        # If no box is defined, raise an exception
        if global_box is None:
            raise Exception("There are not vertices to print.")

        img = Image.new("RGB", [400, 400], "white")
        img_draw = ImageDraw.Draw(img, "RGBA")

        for polygon in polygon_list:
            color = polygon.get_color()
            points = polygon.get_vertices()
            img_draw.polygon(get_draw_coordinates(global_box, points), fill=color + (50,), outline=color + (255,))

        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save(filename)

    @staticmethod
    def random(number_of_vertices):
        point_list = []
        for _ in range(number_of_vertices):
            point_list.append((random(), random()))
        return ConvexPolygon(point_list)
