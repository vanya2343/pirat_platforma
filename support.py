import pygame
from os import walk

def import_folder(path):
    surface_list = []
    for _,__,i in walk(path):
        for image in i:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path)#.convert_alpha()
            surface_list.append(image_surf)
    return surface_list
print(import_folder("grafiks/character/jump"))