import sys

import pygame
import requests

x = 38.205085
y = 44.419486
z = 17

params_for_map = {}


def draw_text(screen, text, x, y):
    font = pygame.font.Font(None, 20)
    text = font.render(text, True, (255, 255, 255))
    text_x, text_y = x, y
    screen.blit(text, (text_x, text_y))


map_files = []

pygame.init()
screen = pygame.display.set_mode((600, 400))
type_ = 'map'
run = True
sat = pygame.Rect((0, 0), (20, 20))
map = pygame.Rect((40, 0), (20, 20))
gbr = pygame.Rect((80, 0), (20, 20))

run = True

while run:
    map_request = f"http://static-maps.yandex.ru/1.x"
    params_for_map['z'] = z
    params_for_map['ll'] = f'{x},{y}'
    params_for_map['l'] = type_
    response = requests.get(map_request, params_for_map)
    rects = [(sat, 'S', 'sat'), (map, 'M', 'map'), (gbr, 'G', 'sat,skl')]
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))

    for i in range(3):
        rect = rects[i][0]
        text = rects[i][1]
        pygame.draw.rect(screen, (0, 0, 0), rect)
        draw_text(screen, text, rect.x + 2, rect.y + 1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP:
                if z != 22:
                    z += 1
            if event.key == pygame.K_UP:
                y += 1
            elif event.key == pygame.K_DOWN:
                y -= 1
            elif event.key == pygame.K_RIGHT:
                x += 1
            elif event.key == pygame.K_LEFT:
                x -= 1
            elif event.key == pygame.K_PAGEDOWN:
                if z != 1:
                    z -= 1
        elif event.type == pygame.MOUSEBUTTONUP:
            rects_ = [i[0] for i in rects]
            for list_ in rects:
                rect = list_[0]
                if rect.collidepoint(event.pos):
                    type_ = list_[2]

pygame.quit()
