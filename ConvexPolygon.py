import math
from PIL import Image, ImageDraw
from functools import cmp_to_key
from random import random
from io import BytesIO


def calc_distance(point_a, point_b) -> float:
    """
    Calcula la distancia entre 2 puntos.

    :param point_a: Punto A.
    :param point_b: Punto B.
    :return: Distancia entre punto A y B.
    """
    return math.sqrt(((point_a[0] - point_b[0]) ** 2) + ((point_a[1] - point_b[1]) ** 2))


def is_inside_2_points(point_a, point_b, point) -> bool:
    """
    Indica si un punto se encuenta dentro de la arista entre A y B.

    :param point_a: Punto A.
    :param point_b: Punto B.
    :param point: Punto a comprobar.
    :return: Booleano indicando si el punto está dentro o no.
    """
    if orientation(point_a, point_b, point) == 0:
        ab_dist = calc_distance(point_a, point_b)
        if ab_dist >= calc_distance(point_a, point) and ab_dist >= calc_distance(point_b, point):
            return True
    return False


def orientation(pa, pb, pc) -> int:
    """
    Calcula el angulo de giro de un punto pc respecto la arista pa-pb.

    :param pa: Primer punto de la arista que conecta con pb
    :param pb: Segundo punto de la arista que contecta ambos puntos
    :param pc: Punto de la arista a comprobar.
    :return: Devuelve la orientación del angulo. 0 --> Colinear | 1 --> Horario | 2 --> Antihorario
    """
    value = (pb[1] - pa[1]) * (pc[0] - pb[0]) - (pb[0] - pa[0]) * (pc[1] - pb[1])
    if value == 0:
        return 0  # Collinear
    elif value > 0:
        return 1  # Clockwise
    else:
        return 2  # Counterclockwise


def convex_hull(points):
    """
    Calcula los puntos que forman un poligono convexo que envuelven a todos los puntos pasados por parametro.

    Algoritmo: Graham Scan
    
    :param points: Lista de puntos.
    :return: La lista de puntos que envuelve a todos los demás en forma de poligono convexo.
    """

    def compare(point0, point1, point2):
        # Funcion que permite ordenar los puntos en sentido horario
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

    if len(points) == 0:
        return points

    # Encuentra el punto más inferior de todos
    ymin = points[0][1]
    min_i = 0
    for i, point in enumerate(points):
        y = point[1]
        if y < ymin or (y == ymin and point[0] < points[min_i][0]):
            ymin = y
            min_i = i

    # Coloca el punto más inferior en la posición inicial
    tmp = points[0]
    points[0] = points[min_i]
    points[min_i] = tmp

    # Ordena los puntos en sentido horario
    points = [points[0]] + sorted(points[1:], key=cmp_to_key(lambda p1, p2: compare(points[0], p1, p2)))

    # Si 2 o más puntos son colineares, eliminaremos todos los puntos entre medio
    # Nota: La función de comparación se encarga de colocar los puntos colineares en orden de distancia
    points_without_collinear = []
    for i in range(len(points)):
        if 1 < i < len(points) - 1 and orientation(points[0], points[i], points[i + 1]) == 0:
            continue
        points_without_collinear.append(points[i])

    points = points_without_collinear

    # Si tenemos menos de 3 vertices, no es necesario calcular más.
    if len(points) < 3:
        return points

    # Se crea una pila inicial con 3 elementos
    stack = []
    for p in points[:3]:
        stack.append(p)

    # Se itera cada elemento para ver si puede formar parte del poligono
    for i in range(3, len(points)):
        while len(stack) >= 2 and orientation(stack[-2], stack[-1], points[i]) != 1:
            stack.pop()
        stack.append(points[i])

    return stack


def get_square_bounding_box(bounding_box):
    """
    Modifica la Bounding Box proporcionada para que tenga relación de aspecto 1:1 (cuadrada) dependiendo de si el ancho o el alto es mayor.
    La Bounding Box se puede obtener con el método get_bounding_box() de ConvexPolygon.

    :param bounding_box: Bounding Box de referencia
    :return: Bounding Box convertida a relación de aspecto  1:1
    """
    xmin = bounding_box[0][0]
    ymin = bounding_box[0][1]

    # Calculate biggest distance in order to create a square box
    dist_x = bounding_box[2][0] - xmin
    dist_y = bounding_box[2][1] - ymin
    dist = (dist_x if dist_x > dist_y else dist_y)

    # Create global bounding box
    return [(xmin, ymin), (xmin, ymin + dist), (xmin + dist, ymin + dist), (xmin + dist, ymin)]


def get_draw_coordinates(square_bounding_box, point_list):
    """
    Transforma la lista de puntos envueltos en la Bounding Box proporcionada para que entren de manera proporcional
    en una Bounding Box de 400x400, correspondiente a las imagenes resultantes de dibujar un ConvexPolygon.

    :param square_bounding_box: Bounding Box con forma cuadrada.
    :param point_list: Lista de puntos a convertir.
    :return: Lista de puntos convertidos a las nuevas corrdenadas.
    """
    def get_point_draw_coordinates(point):
        def get_proportion_dist(coord, initial_coord, dist):
            return float((coord - initial_coord) / dist)

        def get_img_point(coord_prop, dist, start):
            return float(coord_prop * dist + start)

        ref_dist = square_bounding_box[2][0] - square_bounding_box[0][0]
        x_proportion_dist = get_proportion_dist(point[0], square_bounding_box[0][0], ref_dist)
        y_proportion_dist = get_proportion_dist(point[1], square_bounding_box[0][1], ref_dist)

        img_max = 398
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

    def __init__(self, points):
        """
        Función de inicialización del Poligono.
        Se forma en base al poligono convexo que envuelve a los puntos proporcionados.

        :param points: Lista de puntos
        """
        self.points = convex_hull(list(dict.fromkeys(points)))
        # Se define también un color por defecto (Cyan)
        self.color = (59, 163, 188)

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

    def get_color(self) -> (int, int, int):
        """
        Devuelve el color definido para dibujar el polígono.

        Por defecto es Cyan.
        :return: Devuelve el color del polígono en forma de Tuple representando RGB.
        """
        return self.color

    def set_color(self, color: (float, float, float)):
        """
        Define el color para dibujar el polígono.

        Por defecto es Cyan.

        :param color: Color RGB con cada elemento del tuple indicando un color en rango [0,1]
        """
        def to_int(num):
            return int(num * 255)

        self.color = tuple(map(to_int, color))

    def get_vertices(self):
        """
        Devuelve la lista de vertices que conforman el polígono.

        :return: Lista de puntos.
        """
        return self.points.copy()

    def number_of_vertices(self) -> int:
        """
        Devuelve la cantidad de vertices que conforman el polígono.

        :return: Número de vertices.
        """
        return len(self.points)

    def get_perimeter(self) -> float:
        """
        Calcula el perimetro del polígono.

        :return: Perimetro
        """
        perimeter_sum = 0
        for dist in self.__distance_list():
            perimeter_sum += dist
        return round(perimeter_sum, 3)

    def is_regular(self) -> bool:
        """
        Calcula si un polígono es regular.

        :return: Booleano indicando si es regular o no.
        """
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
        """
        Calcula la union convexa de dos poligonos.

        :param convex_polygon: ConvexPolygon a unir.
        :return: ConvexPolygon resultante
        """
        unified_points = self.get_vertices() + convex_polygon.get_vertices()
        return ConvexPolygon(unified_points)

    def contains_convex_polygon(self, convex_polygon) -> bool:
        """
        Calcula si el polígono proporcionado puede ser englobado por este o no.

        :param convex_polygon: ConvexPolygon a comprobar.
        :return: Booleano indicando si el poligono está incluido o no.
        """
        unified_points = self.get_vertices() + convex_polygon.get_vertices()
        union = ConvexPolygon(unified_points)
        return union.get_vertices() == self.get_vertices()

    def intersect(self, convex_polygon):
        """
        Calcula la intersección entre dos polígonos.
        Algoritmo: Sutherland-Hodgman.

        :param convex_polygon: ConvexPolygon a intersectar.
        :return: ConvexPolygon resultante.
        """
        def inside(p):
            orient = orientation(last_clip_vertex, actual_clip_vertex, p)
            if orient == 0 and not is_inside_2_points(last_clip_vertex, actual_clip_vertex, p):
                return False
            return orient != 2

        def computeIntersection():
            dc = [last_clip_vertex[0] - actual_clip_vertex[0], last_clip_vertex[1] - actual_clip_vertex[1]]
            dp = [last_vertex[0] - actual_vertex[0], last_vertex[1] - actual_vertex[1]]
            n1 = last_clip_vertex[0] * actual_clip_vertex[1] - last_clip_vertex[1] * actual_clip_vertex[0]
            n2 = last_vertex[0] * actual_vertex[1] - last_vertex[1] * actual_vertex[0]
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return (n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3

        clip_polygon = convex_polygon.get_vertices()
        output_list = self.get_vertices()
        last_clip_vertex = clip_polygon[-1]

        if self.number_of_vertices() == 0:
            return convex_polygon
        if convex_polygon.number_of_vertices() == 0:
            return self

        for actual_clip_vertex in clip_polygon:
            input_list = output_list
            output_list = []
            last_vertex = input_list[-1]

            for actual_vertex in input_list:
                if inside(actual_vertex):
                    if not inside(last_vertex):
                        output_list.append(computeIntersection())
                    output_list.append(actual_vertex)
                elif inside(last_vertex):
                    output_list.append(computeIntersection())
                last_vertex = actual_vertex
            last_clip_vertex = actual_clip_vertex

        return ConvexPolygon(output_list)

    def contains_point(self, point) -> bool:
        """
        Calcula si el punto proporcionado está contenido por el polígono.

        :param point: Punto a comprobar
        :return: Booleano indicando si el punto está contenido o no.
        """
        if self.number_of_vertices() == 1:
            return self.points[0] == point

        for i in range(self.number_of_vertices()):
            if 0 < i < self.number_of_vertices() - 1:
                orient = orientation(self.points[i], self.points[i + 1], point)
                if orient == 2:
                    return False
                elif orient == 0 and not is_inside_2_points(self.points[i], self.points[i + 1], point):
                    return False
        return True

    def get_centroid(self) -> (float, float):
        """
        Calcula el punto centroide del polígono.

        :return: Punto centroide. Si el polígono tiene menos de 3 vertices devuelve None.
        """
        if self.number_of_vertices() < 3:
            return None

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
        """
        Calcula el area del polígono.

        :return: Area del polígono. Si el polígono tiene menos de 3 vertices devuelve None.
        """
        if self.number_of_vertices() < 3:
            return 0

        area = 0
        j = self.number_of_vertices() - 1

        for i in range(self.number_of_vertices()):
            area += (self.points[j][0] + self.points[i][0]) * (self.points[j][1] - self.points[i][1])
            j = i

        return round(abs(area / 2.0), 3)

    def get_bounding_box(self):
        """
        Calcula el polígono rectangular que envuelve al polígono.

        :return: Lista de 4 puntos.
        """
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

    def draw_polygon(self, filename: str):
        """
        Guarda una imagen del polígono en el archivo con el nombre proporcionado por parámetro.

        :param filename: Nombre de la imagen (Debe incluir la extensión .png)
        """
        b_box = get_square_bounding_box(self.get_bounding_box())

        img = Image.new("RGB", [400, 400], "white")
        img_draw = ImageDraw.Draw(img, "RGBA")
        drawing_points = get_draw_coordinates(b_box, self.points)
        for point in drawing_points:
            img_draw.point(point, fill=self.color + (255,))
        img_draw.polygon(drawing_points, fill=self.color + (50,), outline=self.color + (255,))
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img.save(filename)

    @staticmethod
    def draw(filename: str, polygon_list, image_handler=None):
        """
        Guarda una imagen con la lista de polígonos proporcionada en el archivo con el nombre proporcionado por parámetro.

        :param filename: Nombre de la imagen (Debe incluir la extensión .png)
        :param polygon_list: Lista de polígonos a dibujar
        :param image_handler: Método para gestionar la imagen en caso de que no se quiera guardar en disco.
        """
        def create_global_box(reference_box):
            xmin = reference_box[0][0]
            ymin = reference_box[0][1]
            xmax = reference_box[2][0]
            ymax = reference_box[2][1]

            # Itera todas las bounding box para crear una que las englobe a todas.
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

        # Buscar la primera Bounding Box disponible
        for i, polygon in enumerate(polygon_list):
            first_box = polygon.get_bounding_box()
            if first_box is not None:
                global_box = create_global_box(first_box)
                break

        # Si no se puede definir ninguna Bounding Box, se lanza error.
        if global_box is None:
            raise Exception("There are not vertices to print.")

        img = Image.new("RGB", [400, 400], "white")
        img_draw = ImageDraw.Draw(img, "RGBA")

        for polygon in polygon_list:
            color = polygon.get_color()
            drawing_points = get_draw_coordinates(global_box, polygon.get_vertices())
            for point in drawing_points:
                img_draw.point(point, fill=color + (255,))
            if len(drawing_points) > 2:
                img_draw.polygon(drawing_points, fill=color + (50,), outline=color + (255,))

        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        if image_handler is not None:
            bio = BytesIO()
            bio.name = filename
            img.save(bio, 'PNG')
            bio.seek(0)
            image_handler(filename, bio)
        else:
            img.save(filename)

    @staticmethod
    def random(number_of_vertices):
        """
        Genera una lista de vertices aleatorios y calcula el ConvexPolygon resultante a partir de esa lista.

        Los vertices estan compresos entre [0,1]^2.

        :param number_of_vertices: Numero de vertices a generar.
        :return: ConvexPolygon resultante.
        """
        point_list = []
        for _ in range(number_of_vertices):
            point_list.append((round(random(), 3), round(random(), 3)))
        return ConvexPolygon(point_list)
