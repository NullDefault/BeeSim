import pygame

menu_image = pygame.image.load("assets/menu_background.png")
inspection_menu = pygame.image.load("assets/inspection_menu.png")

pygame.font.init()
gameFont = pygame.font.Font("assets/Retro Gaming.ttf", 18)

fps_location = (20, 800)
bee_number_location = (20, 820)
inspection_menu_location = (50, 300)


def menu_render(entity_master, game_clock, inspection_target):
    menu_surface = pygame.Surface((400, 900))
    menu_surface.blit(menu_image, (0, 0))

    if inspection_target is not None:
        inspection_menu_surface = pygame.Surface((300, 300))
        inspection_menu_surface.blit(inspection_menu, (0, 0))

        bees_total = inspection_target.get_bees()
        bees_total_text = gameFont.render("Hive Population: "+str(bees_total[0]+bees_total[1]), False, [0, 0, 0], None)
        inspection_menu_surface.blit(bees_total_text, (10, 10))

        worker_text = gameFont.render("Workers: "+str(bees_total[0]), False, [0, 0, 0], None)
        inspection_menu_surface.blit(worker_text, (10, 25))

        scout_text = gameFont.render("Scouts: "+str(bees_total[1]), False, [0, 0, 0], None)
        inspection_menu_surface.blit(scout_text, (10, 40))

        hive_nectar = inspection_target.get_nectar()
        nectar_text = gameFont.render("Nectar Storage: "+str(hive_nectar), False, [0, 0, 0], None)
        inspection_menu_surface.blit(nectar_text, (10, 55))

        menu_surface.blit(inspection_menu_surface, inspection_menu_location)

    menu_surface.blit(update_fps_display(game_clock), fps_location)
    menu_surface.blit(number_of_bees(entity_master), bee_number_location)

    return menu_surface


def number_of_bees(entity_master):
    bee_num = entity_master.get_bee_population()
    render = gameFont.render("Bee Population: "+str(bee_num), False, [0, 0, 0], None)
    return render


def update_fps_display(game_clock):
    fps = game_clock.get_fps()
    fps_display = gameFont.render("FPS: "+str(fps)[0:4], False, [0, 0, 0], None)
    return fps_display