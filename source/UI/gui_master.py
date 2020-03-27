"""
Class Name: GuiMaster
Class Purpose: Handles everything UI related.
Notes:
"""
# IMPORTS
from os.path import join

import pygame_gui
from pygame import Rect, USEREVENT, MOUSEBUTTONUP, mouse, Vector2, MOUSEBUTTONDOWN

# CLASS BODY
main_theme = join('source', 'assets', 'gui_theme.json')


class GuiMaster:
    def __init__(self, screen_resolution, entity_master, game_clock):
        self.gui_manager = pygame_gui.UIManager(screen_resolution, main_theme)

        self.entity_master = entity_master
        self.game_clock = game_clock
        self.main_menu_active = False
        self.main_menu_button = pygame_gui.elements.UIButton(relative_rect=
                                                             Rect((screen_resolution[0] - 112,
                                                                   screen_resolution[1] - 112), (110, 110)),
                                                             text='',
                                                             manager=self.gui_manager,
                                                             tool_tip_text="Menu")
        self.menu_size = screen_resolution
        self.drag_begin = None
        self.menu_display = None
        self.bee_num = None
        self.flower_num = None
        self.fps = None

    def update(self, time_delta):
        if self.main_menu_active:
            self.update_main_menu()
        self.gui_manager.update(time_delta)

    def draw_ui(self, screen):
        self.gui_manager.draw_ui(screen)

    def process_events(self, event, camera):
        if event.type == MOUSEBUTTONUP:
            test_position = mouse.get_pos()
            test_position = test_position[0] + camera.location[0], test_position[1] + camera.location[1]
            selected_hive = self.entity_master.get_hive_at(test_position)
            if selected_hive is not None:
                selected_hive.highlight_bees()

            if event.button == 1:
                drag_end = Vector2(event.pos)
                drag_direction = self.drag_begin - drag_end
                camera.move(drag_direction)

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                self.drag_begin = Vector2(mouse_x, mouse_y)

        elif event.type == USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == self.main_menu_button:
                    if self.main_menu_active:
                        self.deactivate_main_menu()
                    else:
                        self.activate_main_menu()
        self.gui_manager.process_events(event)

    def activate_main_menu(self):
        self.main_menu_active = True
        self.menu_display = self.build_menu_display()

    def deactivate_main_menu(self):
        self.main_menu_active = False
        self.menu_display.kill()

    def build_menu_display(self):
        """
        Builds the ui element displaying the current state of the simulation
        :return: Menu render
        """
        number_of_bees = "Number of Bees: " + str(self.entity_master.bee_population)
        number_of_flowers = "Number of Flowers: " + str(self.entity_master.flower_population)
        fps_string = "Frames per Second: " + str(self.game_clock.get_fps())[0:4]

        menu = pygame_gui.core.UIContainer(
            manager=self.gui_manager,
            relative_rect=Rect(0, 0, self.menu_size[0], self.menu_size[1])
        )
        self.bee_num = pygame_gui.elements.UITextBox(
            html_text=number_of_bees,
            relative_rect=Rect(self.menu_size[0] - 275, 25, 250, 50),
            manager=self.gui_manager
        )
        self.flower_num = pygame_gui.elements.UITextBox(
            html_text=number_of_flowers,
            relative_rect=Rect(self.menu_size[0] - 275, 75, 250, 50),
            manager=self.gui_manager
        )
        self.fps = pygame_gui.elements.UITextBox(
            html_text=fps_string,
            relative_rect=Rect(self.menu_size[0] - 275, 125, 250, 50),
            manager=self.gui_manager
        )

        menu.add_element(self.bee_num)
        menu.add_element(self.flower_num)
        menu.add_element(self.fps)

        return menu

    def update_main_menu(self):
        """
        Updates all the parameters that have changed since last time
        :return: void
        """
        fps_string = "Frames per Second: " + str(self.game_clock.get_fps())[0:4]
        self.menu_display.remove_element(self.fps)
        self.fps.kill()
        self.fps = pygame_gui.elements.UITextBox(
            html_text=fps_string,
            relative_rect=Rect(self.menu_size[0] - 275, 125, 250, 50),
            manager=self.gui_manager
        )
        self.menu_display.add_element(self.fps)
