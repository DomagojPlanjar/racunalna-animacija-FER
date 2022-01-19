import math
import sys, time
import numpy as np
import pyglet
from numpy import double
from pyglet.gl import glViewport, glMatrixMode, glLoadIdentity, glOrtho, glBegin, GL_LINE_STRIP, glVertex2i, glEnd, gl, \
    glPushMatrix, glPopMatrix, glRotatef, glVertex3i, gluPerspective, GL_MODELVIEW, glClearColor, glClear, \
    GL_COLOR_BUFFER_BIT, glColor3f, glVertex3f, GL_LINES, glVertex2f, glTranslatef, glEnable, GL_DEPTH_TEST, \
    GL_DEPTH_BUFFER_BIT, GL_PROJECTION, gluOrtho2D, glFlush, glPointSize, GL_POINTS
from numpy import linalg

polygons = list()
vertices = list()


class Vertex:
    def __init__(self, x, y, z, n=None, sumx=0, sumy=0, sumz=0, Nx=0, Ny=0, Nz=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.x) +", "+str(self.y)+", "+str(self.z)

class Polygon:
    def __init__(self, p1, p2, p3, A=0, B=0, C=0, D=0):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self):
        return str(self.p1) +" "+str(self.p2) +" "+str(self.p3)

# Enter your file path as first argument
file = open('C:\\Users\\domag\\PycharmProjects\\RacAniPrviLabos\\kocka.txt', 'r', encoding="utf-8")

verticesCount = 0
polygonsCount = 0
middle = np.array([0.0, 0.0, 0.0])

for line in file:
    currentLine = line.split(" ")

    if line.startswith("#"):
        print("Komentar: "+line)
        continue
    if line.startswith("g"):
        print("Tip: "+line)
        continue

    if line.startswith("v"):
        verticesCount += 1
        x = double(currentLine[1])
        y = double(currentLine[2])
        z = double(currentLine[3])
        vertices.append(Vertex(x, y, z))
        middle[0] += x
        middle[1] += y
        middle[2] += z
        continue

    if line.startswith("f"):
        polygonsCount += 1
        p1 = vertices[int(currentLine[1])-1]
        p2 = vertices[int(currentLine[2])-1]
        p3 = vertices[int(currentLine[3])-1]
        polygons.append(Polygon(p1, p2, p3))

print("Ukupno ima: "+str(verticesCount)+" vrhova i "+str(polygonsCount)+" poligona")
middle[0] /= verticesCount
middle[1] /= verticesCount
middle[2] /= verticesCount
print("Središte objekta jest: "+str(middle[0])+" "+str(middle[1])+" "+str(middle[2]))

file_curve = open('C:\\Users\\domag\\PycharmProjects\\RacAniPrviLabos\\spirala.txt', 'r', encoding="utf-8")
curve_control_points = list()
control_points_count = 0

for line in file_curve:
    currentLine = line.split(" ")
    if line.startswith("v"):
        x = double(currentLine[1])
        y = double(currentLine[2])
        z = double(currentLine[3])
        curve_control_points.append(Vertex(x, y, z))
        control_points_count += 1

number_of_segments = control_points_count - 3

cubic_b_matrix = np.array([[-1, 3, -3, 1],
                         [3, -6, 3, 0],
                         [-3, 0, 3, 0],
                         [1, 4, 1, 0]])

tangent_b_matrix = np.array([[-1, 3, -3, 1],
                            [2, -4, 2, 0],
                            [-1, 0, 1, 0]])

object_points = list()
segment_points = list()
segment_tangents = list()
segment_rotations = list()
rotation_axis = np.array([0, 0, 0])
first_control_point_index = 0


def calculating_animations():
    global segment_rotations, segment_points, segment_tangents
    global rotation_axis, first_control_point_index
    segment_count = 0

    while True:

        curr_segment = list()
        flag = False

        if segment_count == number_of_segments:
            break

        for index in range(first_control_point_index, first_control_point_index+4):
            curr_segment.append(curve_control_points[index])

        if flag:
            break

        segment_count += 1

        #print("Izašao sam 1 put")
        first_control_point_index += 1
        t = 0
        step = 0.01
        const = 1 / 6
        s = np.array([0, 0, 1])

        while t<1:
            parameter_vector = np.array([math.pow(t, 3), math.pow(t, 2), t, 1])
            control_point_vector = np.array([[curr_segment[0].x, curr_segment[0].y, curr_segment[0].z],
                                              [curr_segment[1].x, curr_segment[1].y, curr_segment[1].z],
                                              [curr_segment[2].x, curr_segment[2].y, curr_segment[2].z],
                                             [curr_segment[3].x, curr_segment[3].y, curr_segment[3].z]])

            segment_point = parameter_vector * const
            segment_point = np.matmul(segment_point, cubic_b_matrix)
            segment_point = np.matmul(segment_point, control_point_vector)
            segment_points.append(segment_point)

            tangent_parameter_vector = np.array([math.pow(t, 2), t, 1])
            tangent_parameter_vector = tangent_parameter_vector * 1/2
            tangent_vector = np.matmul(tangent_parameter_vector, tangent_b_matrix)
            tangent_vector = np.matmul(tangent_vector, control_point_vector)                # izračun tangente
            segment_tangents.append(segment_point)                                          # početna
            tangent_vector_next = segment_tangents[-1] + tangent_vector/3                   # ciljna
            segment_tangents.append(tangent_vector_next)



            rotation_axis = np.cross(s, tangent_vector)                                                         #rotacijska os (početni i ciljni vektor)
            cos_rotation_angle = np.dot(s, tangent_vector) / (linalg.norm(s) * linalg.norm(tangent_vector))     #rotacijski kut
            rotation_angle_rad = math.acos(cos_rotation_angle)
            rotation_angle_degrees = math.degrees(rotation_angle_rad)



            segment_rotations.append(rotation_angle_degrees)
            t += step



window = pyglet.window.Window(width = 800, height = 650, resizable = True)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

a = 0
e = np.array([0, 0, 0])
s = np.array([0, 0, 1])
os = np.array([0, 0, 0])


def update_parameter(self):
    global a
    a += 1
    if a == 100 * number_of_segments:
        a = 0


@window.event
def on_resize(width, height):
    window.invalid = True
    print ("Pozvan on_resize()\n")

    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 0.1, 100)
    glMatrixMode(gl.GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, width, height)

@window.event
def on_draw():
    global pos_z, rot_y, a

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, 1, 0.1, 100)
    glColor3f(0, 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLoadIdentity()
    glTranslatef(*pos)
    glRotatef(rot_y, 0, 1, 0)

    # crtanje krivulje
    glBegin(GL_LINE_STRIP)
    count = 0
    for i in range(0, number_of_segments * 100):
        glVertex3f(segment_points[i][0] / 5, segment_points[i][1] / 5, segment_points[i][2] / 5)  # točke na krivulji
        count += 1
    glEnd()

    # crtanje tangenti
    glBegin(GL_LINES)
    for i in range(0, number_of_segments * 100 * 2, 25):
        glVertex3f(segment_tangents[i][0] / 5, segment_tangents[i][1] / 5, segment_tangents[i][2] / 5)
        glVertex3f(segment_tangents[i + 1][0] / 5, segment_tangents[i + 1][1] / 5, segment_tangents[i + 1][2] / 5)
    glEnd()

    glTranslatef(segment_points[a][0] / 5, segment_points[a][1] / 5, segment_points[a][2] / 5)

    e[0] = segment_tangents[2 * a + 1][0] - segment_tangents[2 * a][0]
    e[1] = segment_tangents[2 * a + 1][1] - segment_tangents[2 * a][1]
    e[2] = segment_tangents[2 * a + 1][2] - segment_tangents[2 * a][2]

    rotation_axis = np.cross(s, e)
    cos_rotation_angle = np.dot(s, e) / (linalg.norm(s) * linalg.norm(e))
    rotation_angle_rad = math.acos(cos_rotation_angle)
    rotation_angle_degrees = math.degrees(rotation_angle_rad)
    #glPushMatrix()
    glRotatef(rotation_angle_degrees, rotation_axis[0], rotation_axis[1], rotation_axis[2])

    glTranslatef(-middle[0], -middle[1], -middle[2])
    glColor3f(0.8, 0.6, 0.1)

    glBegin(GL_LINES)

    for i in range(0, polygonsCount):
        vertex_one = polygons[i].p1
        vertex_two = polygons[i].p2
        vertex_three = polygons[i].p3
        glVertex3f(vertex_one.x, vertex_one.y, vertex_one.z)
        glVertex3f(vertex_two.x, vertex_two.y, vertex_two.z)

        glVertex3f(vertex_two.x, vertex_two.y, vertex_two.z)
        glVertex3f(vertex_three.x, vertex_three.y, vertex_three.z)

        glVertex3f(vertex_three.x, vertex_three.y, vertex_three.z)
        glVertex3f(vertex_one.x, vertex_one.y, vertex_one.z)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(middle[0], middle[1], middle[2])
    glVertex3f(middle[0] + 2.5, middle[1], middle[2])

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(middle[0], middle[1], middle[2])
    glVertex3f(middle[0], middle[1] + 2.5, middle[2])

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(middle[0], middle[1], middle[2])
    glVertex3f(middle[0], middle[1], middle[2] + 2.5)

    glColor3f(0.0, 0.0, 0.0)
    glEnd()


pos = [0, 0, -20]
rot_y = 0



@window.event
def on_key_press(s, m):

    global pos_z, rot_y

    if s == pyglet.window.key.W:
        pos[2] -= 1
    if s == pyglet.window.key.S:
        pos[2] += 1
    if s == pyglet.window.key.A:
        rot_y += 5
    if s == pyglet.window.key.D:
        rot_y -= 5



if __name__ == "__main__":
    window.set_location(100, 40)
    calculating_animations()
    pyglet.clock.schedule_interval(update_parameter, 1/100)
    pyglet.app.run()



