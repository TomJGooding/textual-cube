from __future__ import annotations

import math

from textual.app import App, ComposeResult
from textual.color import Color
from textual_canvas import Canvas

"""Code for rendering and rotating the cube adapted from
https://github.com/asciimoo/drawille
"""


class Point3D:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def project_to_2D(
        self,
        width: float,
        height: float,
        field_of_view: float,
        viewer_distance: float,
    ) -> Point3D:
        factor = field_of_view / (viewer_distance + self.z)
        x = self.x * factor + width / 2
        y = -self.y * factor + height / 2
        return Point3D(x, y, 1)

    def rotate_x(self, angle: float) -> Point3D:
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotate_y(self, angle: float) -> Point3D:
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotate_z(self, angle: float) -> Point3D:
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)


class Cube:
    """This cube diagram shows the index of each vertex in the VERTICES list:

       3-------2
      /|      /|
     7-------6 |
     | |     | |
     | 0-----|-1
     |/      |/
     4-------5

    Each cube face is composed of four vertices. The six faces of the cube are
    defined in FACES, where the numbers refer to the index in the VERTICES list.
    """

    VERTICES = [
        Point3D(-10, 10, -10),  # vertex 0
        Point3D(10, 10, -10),  # vertex 1
        Point3D(10, -10, -10),  # vertex 2
        Point3D(-10, -10, -10),  # vertex 3
        Point3D(-10, 10, 10),  # vertex 4
        Point3D(10, 10, 10),  # vertex 5
        Point3D(10, -10, 10),  # vertex 6
        Point3D(-10, -10, 10),  # vertex 7
    ]

    FACES = [
        (0, 1, 2, 3),
        (1, 5, 6, 2),
        (5, 4, 7, 6),
        (4, 0, 3, 7),
        (0, 4, 5, 1),
        (3, 2, 6, 7),
    ]

    def __init__(self) -> None:
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    @property
    def vertices_2D(self) -> list[Point3D]:
        vertices_2D: list[Point3D] = []
        for vertex in self.VERTICES:
            point = (
                vertex.rotate_x(self.angle_x)
                .rotate_y(self.angle_y)
                .rotate_z(self.angle_z)
            )
            vertices_2D.append(
                point.project_to_2D(
                    width=50,
                    height=50,
                    field_of_view=50,
                    viewer_distance=50,
                )
            )
        return vertices_2D

    def rotate(self) -> None:
        self.angle_x += 2
        self.angle_y += 3
        self.angle_z += 5


class CubeApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    Canvas {
        width: auto;
        height: auto;
    }
    """

    cube = Cube()

    def compose(self) -> ComposeResult:
        yield Canvas(50, 50)

    def on_mount(self) -> None:
        self.draw_cube()
        self.set_interval(1 / 20, self.rotate_cube)

    def rotate_cube(self) -> None:
        self.cube.rotate()
        self.clear_canvas()
        self.draw_cube()

    def draw_cube(self) -> None:
        canvas = self.query_one(Canvas)
        for face in self.cube.FACES:
            canvas.draw_line(
                x0=round(self.cube.vertices_2D[face[0]].x),
                y0=round(self.cube.vertices_2D[face[0]].y),
                x1=round(self.cube.vertices_2D[face[1]].x),
                y1=round(self.cube.vertices_2D[face[1]].y),
                color=Color(255, 255, 255),
            )
            canvas.draw_line(
                x0=round(self.cube.vertices_2D[face[1]].x),
                y0=round(self.cube.vertices_2D[face[1]].y),
                x1=round(self.cube.vertices_2D[face[2]].x),
                y1=round(self.cube.vertices_2D[face[2]].y),
                color=Color(255, 255, 255),
            )
            canvas.draw_line(
                x0=round(self.cube.vertices_2D[face[2]].x),
                y0=round(self.cube.vertices_2D[face[2]].y),
                x1=round(self.cube.vertices_2D[face[3]].x),
                y1=round(self.cube.vertices_2D[face[3]].y),
                color=Color(255, 255, 255),
            )
            canvas.draw_line(
                x0=round(self.cube.vertices_2D[face[3]].x),
                y0=round(self.cube.vertices_2D[face[3]].y),
                x1=round(self.cube.vertices_2D[face[0]].x),
                y1=round(self.cube.vertices_2D[face[0]].y),
                color=Color(255, 255, 255),
            )

    def clear_canvas(self) -> None:
        # The textual-canvas library unfortunately doesn't have a Canvas.clear
        # method, so we have to hand-roll our own
        canvas = self.query_one(Canvas)
        canvas._canvas = [
            [Color(0, 0, 0) for _ in range(canvas._width)]
            for _ in range(canvas._height)
        ]
        canvas.refresh()


if __name__ == "__main__":
    app = CubeApp()
    app.run()
