import pygame

BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
DARK_GREY = (64, 64, 64)
light_turq = (175, 238, 238)
dark_turq = (0, 128, 128)
light_grey = (200, 200, 200)
dark_grey = (100, 100, 100)


def adjust_mouse_pos(mouse_x, x, radius, board_w, buffer):
    if mouse_x < x + radius + buffer:
        return x + radius + buffer
    elif mouse_x > x + board_w - radius - buffer:
        return x + board_w - radius - buffer
    return mouse_x


def create_gradient_circle(radius, outer_color, inner_color):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        color = (
            int(outer_color[0] + (inner_color[0] - outer_color[0]) * (r / radius)),
            int(outer_color[1] + (inner_color[1] - outer_color[1]) * (r / radius)),
            int(outer_color[2] + (inner_color[2] - outer_color[2]) * (r / radius))
        )
        pygame.gfxdraw.filled_circle(surface, radius, radius, r, color)
    return surface
