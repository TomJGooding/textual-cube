from __future__ import annotations

from textual.app import App, ComposeResult
from textual.color import Color
from textual_canvas import Canvas

"""Code for rendering the cube adapted from
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

FACES = [
    (0, 1, 2, 3),
    (1, 5, 6, 2),
    (5, 4, 7, 6),
    (4, 0, 3, 7),
    (0, 4, 5, 1),
    (3, 2, 6, 7),
]


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

    def compose(self) -> ComposeResult:
        yield Canvas(50, 50)

    def on_mount(self) -> None:
        vertices_2D: list[Point3D] = []
        for vertex in VERTICES:
            vertices_2D.append(
                vertex.project_to_2D(
                    width=50,
                    height=50,
                    field_of_view=50,
                    viewer_distance=50,
                )
            )

        canvas = self.query_one(Canvas)
        for face in FACES:
            canvas.draw_line(
                x0=round(vertices_2D[face[0]].x),
                y0=round(vertices_2D[face[0]].y),
                x1=round(vertices_2D[face[1]].x),
                y1=round(vertices_2D[face[1]].y),
                color=Color(255, 255, 255),
            )
            canvas.draw_line(
                x0=round(vertices_2D[face[1]].x),
                y0=round(vertices_2D[face[1]].y),
                x1=round(vertices_2D[face[2]].x),
                y1=round(vertices_2D[face[2]].y),
                color=Color(255, 255, 255),
            )
            canvas.draw_line(
                x0=round(vertices_2D[face[2]].x),
                y0=round(vertices_2D[face[2]].y),
                x1=round(vertices_2D[face[3]].x),
                y1=round(vertices_2D[face[3]].y),
                color=Color(255, 255, 255),
            )
            canvas.draw_line(
                x0=round(vertices_2D[face[3]].x),
                y0=round(vertices_2D[face[3]].y),
                x1=round(vertices_2D[face[0]].x),
                y1=round(vertices_2D[face[0]].y),
                color=Color(255, 255, 255),
            )


if __name__ == "__main__":
    app = CubeApp()
    app.run()
