import math
from typing import (
    List,
    Tuple
)

import click
import pygame.gfxdraw
from pygame import Rect
from pytouch_c import (
    f_viewcoordinate
)

from objects import (
    Mesh,
    ObjMesh,
    Text
)
from utils import gif_create
from loguru import logger


class Camera:
    def __init__(self, viewport_rect: Rect, position: Tuple[float, float, float], rotation: Tuple[float, float]):
        self.viewport_rect = viewport_rect
        self.position = position
        self.rotation = rotation

    def events(self, event):
        self.rotation = (
            self.rotation[0] + event.rel[1] * 2 / self.viewport_rect.width,
            self.rotation[1] + event.rel[0] * 2 / self.viewport_rect.height
        )

    def update(self, dt: float, vector: Tuple[float, float, float]):
        s = dt * 10
        x, y = math.sin(self.rotation[1]), math.cos(self.rotation[1])

        self.position = (
            self.position[0] + s * (x * vector[1] + y * vector[0]),
            self.position[1] + s * vector[2],
            self.position[2] + s * (y * vector[1] - x * vector[0])
        )

    def viewcoordinate(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        return f_viewcoordinate(*self.position, x, y, z, *self.rotation)

    def project(self, x: float, y: float, z: float):
        f = 200 / z if z else 200000
        return (
            self.viewport_rect.centerx + round(x * f),
            self.viewport_rect.centery + round(y * f)
        )

    def clip_near(self, x: float, y: float, z: float):
        near = 0.5
        if z >= near:
            return

        nearscale = 200 / near
        return (
            self.viewport_rect.centerx + round(x * nearscale),
            self.viewport_rect.centery + round(y * nearscale)
        )


def get_meshes() -> List[Mesh]:
    # noinspection PyListCreation
    meshes: List[Mesh] = []

    meshes.append(
        Text.from_string(
            string='Поставте 60 :)',
            position=(0, 0, 0),
            colors=[],
            font='C:\\Windows\\Fonts\\arial.ttf'
        )
    )

    # sphere = Sphere(pos=(0,10,0), radius=10, widthSegments=64, heightSegments=64)
    #
    # heart = ObjMesh.from_file(
    #     file_path='models/teddy.obj',
    #     position=(70, -30, 0),
    #     colors=[]
    # )
    # heart.angle_z = 0
    # heart.angle_x = 270
    # heart.angle_y = 180
    # heart.scale(5)
    # heart.rebuild()
    #
    # for index in range(3):
    #     hear_duplicate = heart.copy()
    #     hear_duplicate.position = (0, 60 + index * 60, 0)
    #     meshes.append(hear_duplicate)

    return meshes


@click.command()
@click.option('target_fps', '--fps', default=60, help='Taget FPS.', type=int)
@click.option('width', '--width', default=1920, help='Screen width.', type=int)
@click.option('height', '--height', default=1080, help='Screen height.', type=int)
@click.option('capture', '--capture', default=False, help='Capture GIF.', is_flag=True)
def main(
    target_fps: int,
    width: int,
    height: int,
    capture: bool
):
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    fps_font = pygame.font.SysFont('Comic Sans MS', 30)
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    clock = pygame.time.Clock()

    camera = Camera(screen.get_rect(), (0, 0, -5), (0, 0))

    meshes = get_meshes()

    screenshot_idx = capture_idx = 0
    run = True

    while run:
        dt = clock.tick(target_fps) / 1000
        fps = 1 / dt

        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type in (
                pygame.QUIT,
                pygame.K_ESCAPE
            ):
                run = False

            if event.type == pygame.MOUSEMOTION:
                camera.events(event)

        key = pygame.key.get_pressed()
        camera.update(
            dt,
            (
                key[pygame.K_d] - key[pygame.K_a],
                key[pygame.K_w] - key[pygame.K_s],
                key[pygame.K_q] - key[pygame.K_e]
            )
        )

        if key[pygame.K_r]:
            camera.position = (0, 0, -5)
            camera.rotation = (0, 0)

        for mesh in meshes:
            mesh.update()

        polygons_count = 0
        order: List[Tuple[int, float, List[Tuple[int, int]], Tuple[int, int, int]]] = []

        for mesh in meshes:
            polygons_count += len(mesh.faces)
            vertex_list = tuple(camera.viewcoordinate(x, y, z) for x, y, z in mesh.verts)
            screen_coordinates = [camera.project(x, y, z) for x, y, z in vertex_list]

            for idx, face in enumerate(mesh.faces):
                clipped = True
                for vertex_index in face:
                    x, y, z = vertex_list[vertex_index]
                    if z <= 0:
                        break

                    screen_x, screen_y = screen_coordinates[vertex_index]

                    if (
                        screen_x < 0 or screen_x > camera.viewport_rect.width or
                        screen_y < 0 or screen_y > camera.viewport_rect.height
                    ):
                        break

                    if coordinates := camera.clip_near(x, y, z):
                        screen_coordinates[vertex_index] = coordinates
                else:
                    clipped = False

                if clipped:
                    continue

                order.append(
                    (
                        idx,
                        sum(vertex_list[j][2] for j in face) / len(face),
                        [screen_coordinates[x] for x in face],
                        mesh.colors[idx]
                    )
                )

        order.sort(key=lambda x: x[1] if x else 0, reverse=True)

        for _, __, screen_coordinates, colors in filter(bool, order):
            try:
                pygame.gfxdraw.filled_polygon(screen, screen_coordinates, colors)
            except Exception as e:
                logger.error(e)

        if key[pygame.K_f]:
            pygame.image.save(screen, f"screenshot_{screenshot_idx}.jpeg")
            screenshot_idx += 1

        fps_string = f'FPS: {fps:.0f}'
        fps_object = fps_font.render(fps_string, True, (0, 255, 0), (0, 0, 128))
        screen.blit(fps_object, (50, 50))

        polygons_count_string = f'Polygons: {len(order)}/{polygons_count}'
        polygons_count_object = fps_font.render(polygons_count_string, True, (0, 255, 0), (0, 0, 128))
        screen.blit(polygons_count_object, (50, 100))

        if capture:
            pygame.image.save(screen, f"capture/capture_{capture_idx}.jpeg")
            capture_idx += 1

        pygame.display.flip()

    pygame.quit()

    if not capture:
        return

    print(f'Compile gif image ( {capture_idx + 1} frames )')
    gif_create('capture/capture_*.jpeg')


if __name__ == '__main__':
    main()
