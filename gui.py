import pygame
import drawing
import event
import media
import menu
import general
import sys


class Screen:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.screen = None
        
    def show(self, x=0, y=0):
        self.parent_screen.blit(self.screen, (x, y))


class MenuScreen(Screen):
    def __init__(self, parent_screen, title_image):
        Screen.__init__(self, parent_screen)
        self.screen = pygame.Surface(parent_screen.get_size())
        menu_canvas = pygame.Surface((1, 1))
        self.menu = menu.Menu(menu_canvas)
        self.menu_handler = event.MenuMouseEventHandler(self.menu)
        self.handler = event.MenuScreenMouseEventHandler(self)
        cursor_image = media.ImageManager.IMG_MenuCursor
        self.cursor = media.ImageManager.image(cursor_image)
        self.cursor_pos = (0, 0)
        self.title_image = title_image
        self.title_y = 50
        
    def add_menu_item(self, action, image):
        self.menu.add(action, image)
        self.show()
        
    def menu_offset(self):
        w, h = self.screen.get_size()
        menu_w, menu_h = self.menu.canvas.get_size()
        menu_x = (w - menu_w) / 2
        menu_y = (h - menu_h) / 2
        return (menu_x, menu_y)
        
    def handle_event(self, e):
        menu_x, menu_y = self.menu_offset()
        try:
            pos = e.pos[0] - menu_x, e.pos[1] - menu_y
            self.cursor_pos = e.pos[0] - media.ImageManager.NUM_MenuCursorTip, e.pos[1]
            ev = event.MouseEvent(e.type, pos)        
            self.menu_handler.handle(ev)
            self.handler.handle(e)
        except AttributeError:
            pass
    
    def move(self, (x, y)):
        self.cursor_pos = x - media.ImageManager.NUM_MenuCursorTip, y
    
    def show(self):
        self.show_nocursor()
        self.screen.blit(self.cursor, self.cursor_pos)
        Screen.show(self)
        
    def show_nocursor(self):
        self.screen.fill((0, 0, 0))
        w, h = self.screen.get_size()
        title_w, title_h = self.title_image.get_size()
        title_x = (w - title_w) / 2
        self.screen.blit(self.title_image, (title_x, self.title_y))
        menu_x, menu_y = self.menu_offset()
        self.menu.paint(self.screen, menu_x, menu_y)
        Screen.show(self)


class MenuPopup(Screen):
    def __init__(self, parent_screen, background=None):
        Screen.__init__(self, parent_screen)
        self.background = background
        self.screen = pygame.Surface((1, 1))
        self.menu = menu.Menu(self.screen)
        self.handler = event.MenuMouseEventHandler(self.menu)
        self.cursor = media.ImageManager.image(media.ImageManager.IMG_MenuCursor)
        self.cursor_pos = background.cursor_pos
        
    def add_menu_item(self, action, image):
        self.menu.add(action, image)
        self.screen = pygame.Surface(self.menu.canvas.get_size())
        self.show()
        
    def menu_offset(self):
        w, h = self.parent_screen.get_size()
        menu_w, menu_h = self.screen.get_size()
        menu_x = (w - menu_w) / 2
        menu_y = (h - menu_h) / 2
        return (menu_x, menu_y)
    
    def handle_event(self, e):
        menu_x, menu_y = self.menu_offset()
        try:
            pos = e.pos[0] - menu_x, e.pos[1] - menu_y
            self.cursor_pos = e.pos[0] - media.ImageManager.NUM_MenuCursorTip, e.pos[1]
            ev = event.MouseEvent(e.type, pos)
            self.handler.handle(ev)
        except AttributeError:
            pass
        
    def show(self):
        menu_x, menu_y = self.menu_offset()
        self.menu.paint(self.screen)
        self.background.show_nocursor()
        Screen.show(self, menu_x, menu_y)
        self.parent_screen.blit(self.cursor, self.cursor_pos)


class MessagePopup(Screen):
    def __init__(self, parent_screen, manager, background=None, color=(0, 0, 0)):
        Screen.__init__(self, parent_screen)
        self.manager = manager
        self.background = background
        self.color = color
        self.screen = pygame.Surface((1, 1))
        self.text_height = 50
        self.x_offset = 10
        self.text = []
        self.cursor = media.ImageManager.image(media.ImageManager.IMG_MenuCursor)
        self.cursor_pos = (0, 0)
        self.key_handler = event.PopupKeyEventHandler(self)
        self.mouse_handler = event.PopupMouseEventHandler(self)
        
        
    def add_text_line(self, text, color=(255, 255, 255)):
        font = media.ImageManager.TTF_MenuItem
        self.text.append(media.ImageManager.text(text, font, color))
        self.resize_canvas()
    
    def resize_canvas(self):
        items_widths = []
        for item in self.text:
            items_widths.append(item.get_rect().w + self.x_offset)
        new_w = max(items_widths) + self.x_offset
        new_h = len(self.text) * self.text_height
        self.screen = pygame.transform.scale(self.screen, (new_w, new_h))
        
    def message_offset(self):
        w, h = self.parent_screen.get_size()
        msg_w, msg_h = self.screen.get_size()
        msg_x = (w - msg_w) / 2
        msg_y = (h - msg_h) / 2
        return (msg_x, msg_y)
    
    def show(self):
        self.background.show_nocursor()
        msg_x, msg_y = self.message_offset()
        self.screen.fill(self.color)
        for i in range(0, len(self.text)):
            self.screen.blit(self.text[i], (self.x_offset, i*self.text_height))
        Screen.show(self, msg_x, msg_y)
        self.parent_screen.blit(self.cursor, self.cursor_pos)
    
    def handle_event(self, e):
        self.key_handler.handle(e)
        self.mouse_handler.handle(e)
    
    def exit(self, arg):
        self.manager.bac_action()
    
    def move(self, (x, y)):
        self.cursor_pos = x - media.ImageManager.NUM_MenuCursorTip, y


class DrawScreen(Screen):
    def __init__(self, parent_screen, manager):
        Screen.__init__(self, parent_screen)
        self.manager = manager
        self.panel = GuiFactory.get_color_panel()
        self.canvas = drawing.DrawCanvas(parent_screen.get_size(), self.panel)
        self.cursor_pos = (0, 0)
        self.cursor = media.ImageManager.image(media.ImageManager.IMG_DoodleCursor)
        self.cursor_change = {}
        self.cursor_change[True] = media.ImageManager.image(media.ImageManager.IMG_MenuCursor)
        self.cursor_change[False] = media.ImageManager.image(media.ImageManager.IMG_DoodleCursor)
        self.sound_change = {}
        self.sound_change[True] = media.AudioManager.SND_ColorSelect
        self.sound_change[False] = media.AudioManager.SND_Pencil
        self.sound_play_mode = {}
        self.sound_play_mode[True] = media.AudioManager.play
        self.sound_play_mode[False] = media.AudioManager.play_music
        self.move_action = None
        self.mouse_handler = event.DrawMouseEventHandler(self)
        self.key_handler = event.DrawKeyEventHandler(self)
    
    def mouse_in_panel(self, (x, y)):
        self.cursor_pos = x, y
        cursor_r = pygame.Rect(x, y, 1, 1)
        panel_r = self.panel.get_rect()
        return cursor_r.colliderect(panel_r)
    
    def draw_point(self, (x, y)):
        self.canvas.add_point((x, y))        
    
    def in_canvas(self, (x, y)):
        self.panel.select((x+media.ImageManager.NUM_MenuCursorTip, y))
        self.move_action = self.draw_point
        self.draw_point((x, y))
        in_panel = self.mouse_in_panel((x, y))
        self.sound_play_mode[in_panel](self.sound_change[in_panel])
    
    def out_canvas(self, (x, y)):
        self.canvas.release_mouse()
        self.move_action = None
        media.AudioManager.stop_music()
    
    def move(self, (x, y)):
        in_panel = self.mouse_in_panel((x, y))
        self.cursor = self.cursor_change[in_panel]
        try:
            self.move_action((x, y))
        except TypeError:
            return
    
    def handle_event(self, e):
        self.mouse_handler.handle(e)
        self.key_handler.handle(e)
    
    def show(self):
        self.show_nocursor()
        self.parent_screen.blit(self.cursor, self.cursor_pos)
    
    def show_nocursor(self):
        self.canvas.paint(self.parent_screen)
        self.panel.paint(self.parent_screen)
    
    def save(self, arg):
        x = self.panel.get_rect().w
        y = 0
        w = self.canvas.w - x
        h = self.canvas.h
        area = pygame.Rect(x, y, w, h)
        self.canvas.save(area)
    
    def clean(self, arg):
        self.canvas.clean()
    
    def pause(self, arg):
        self.manager.draw_menu()


class GuiManager:
    def __init__(self):
        self.gui_stack = general.Stack()
        self.resolution = (640, 480)
        self.screen_flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN
        self.init_screen()

    def main_menu(self):
        self.init_screen()
        self.gui_stack.empty()
        self.gui_stack.push(GuiFactory.get_main_menu(self))
        self.show_current()
    
    def draw_menu(self):
        self.gui_stack.push(GuiFactory.get_draw_menu(self))
        self.show_current()
    
    def doo_action(self):
        cursor_pos = self.gui_stack.top().cursor_pos
        self.init_screen(self.resolution)
        self.gui_stack.push(GuiFactory.get_draw_screen(self))
        self.gui_stack.top().cursor_pos = cursor_pos
        self.show_current()
    
    def opt_action(self):
        cursor_pos = self.gui_stack.top().cursor_pos
        self.gui_stack.push(GuiFactory.get_opt_menu(self))
        self.gui_stack.top().cursor_pos = cursor_pos
        self.show_current()
    
    def opt_sou_action(self):
        cursor_pos = self.gui_stack.top().cursor_pos
        self.gui_stack.push(GuiFactory.get_sou_menu(self))
        self.gui_stack.top().cursor_pos = cursor_pos
        self.show_current()
    
    def opt_sou_on_action(self):
        media.AudioManager.on()
        self.bac_action()
    
    def opt_sou_off_action(self):
        media.AudioManager.off()
        self.bac_action()
    
    def opt_res_action(self):
        cursor_pos = self.gui_stack.top().cursor_pos
        self.gui_stack.push(GuiFactory.get_opt_res_menu(self))
        self.gui_stack.top().cursor_pos = cursor_pos
        self.show_current()
    
    def opt_res_low_action(self):
        self.resolution = (640, 480)
        self.bac_action()
    
    def opt_res_med_action(self):
        self.resolution = (800, 600)
        self.bac_action()
    
    def opt_res_hig_action(self):
        self.resolution = (1024, 768)
        self.bac_action()
    
    def abo_action(self):
        cursor_pos = self.gui_stack.top().cursor_pos
        self.gui_stack.push(GuiFactory.get_abo_screen(self))
        self.gui_stack.top().cursor_pos = cursor_pos
        self.show_current()
    
    def bac_action(self):
        try:
            cursor_pos = self.gui_stack.top().cursor_pos
        except AttributeError:
            cursor_pos = 0, 0
        self.gui_stack.pop()
        self.gui_stack.top().cursor_pos = cursor_pos
        self.show_current()
    
    def handle_event(self, e):
        self.gui_stack.top().handle_event(e)
    
    def show_current(self):
        self.gui_stack.top().show()
    
    def init_screen(self, resolution=(640, 480)):
        self.screen = pygame.display.set_mode(resolution, self.screen_flags, 32)


class GuiFactory:
    @staticmethod
    def get_color_panel():
        panel = drawing.ColorPanel()
        panel.add_color_item(drawing.ColorItem(media.COL_Black))
        panel.add_color_item(drawing.ColorItem(media.COL_Pink))
        panel.add_color_item(drawing.ColorItem(media.COL_Red))
        panel.add_color_item(drawing.ColorItem(media.COL_Wine))
        panel.add_color_item(drawing.ColorItem(media.COL_LightBlue))
        panel.add_color_item(drawing.ColorItem(media.COL_Blue))
        panel.add_color_item(drawing.ColorItem(media.COL_Yellow))
        panel.add_color_item(drawing.ColorItem(media.COL_LightGreen))
        panel.add_color_item(drawing.ColorItem(media.COL_DarkGreen))
        panel.add_color_item(drawing.ColorItem(media.COL_LightGray))
        panel.add_color_item(drawing.ColorItem(media.COL_DarkGray))
        panel.add_color_item(drawing.ColorItem(media.COL_Orange))
        panel.add_color_item(drawing.ColorItem(media.COL_Purple))
        panel.add_color_item(drawing.ColorItem(media.COL_LightBrown))
        panel.add_color_item(drawing.ColorItem(media.COL_DarkBrown))
        panel.add_color_item(drawing.ColorItem(media.COL_Skin))
        return panel

    @staticmethod
    def get_main_menu(manager):
        font = media.ImageManager.TTF_Title
        color = media.COL_Blue
        title = media.ImageManager.text("PyDoodler", font, color, 64)
        menu = MenuScreen(manager.screen, title)
        font = media.ImageManager.TTF_MenuItem
        color = media.COL_Red
        image = media.ImageManager.text("Doodle!", font, color)
        menu.add_menu_item(manager.doo_action, image)
        image = media.ImageManager.text("Options", font, color)
        menu.add_menu_item(manager.opt_action, image)
        image = media.ImageManager.text("About", font, color)
        menu.add_menu_item(manager.abo_action, image)
        image = media.ImageManager.text("Quit", font, color)
        menu.add_menu_item(sys.exit, image)
        return menu
    
    @staticmethod
    def get_draw_menu(manager):
        menu = MenuPopup(manager.screen, manager.gui_stack.top())
        font = media.ImageManager.TTF_MenuItem
        color = media.COL_White
        image = media.ImageManager.text("Continue doodling", font, color)
        menu.add_menu_item(manager.bac_action, image)
        image = media.ImageManager.text("Main menu", font, color)
        menu.add_menu_item(manager.main_menu, image)
        image = media.ImageManager.text("Quit", font, media.COL_DarkGreen)
        menu.add_menu_item(sys.exit, image)
        return menu
    
    @staticmethod
    def get_draw_screen(manager):
        return DrawScreen(manager.screen, manager)
    
    @staticmethod
    def get_opt_menu(manager):
        font = media.ImageManager.TTF_Title
        color = media.COL_Blue
        title = media.ImageManager.text("Options", font, color, 64)
        menu = MenuScreen(manager.screen, title)
        font = media.ImageManager.TTF_MenuItem
        color = media.COL_Red
        image = media.ImageManager.text("Sound", font, color)
        menu.add_menu_item(manager.opt_sou_action, image)
        image = media.ImageManager.text("Resolution", font, color)
        menu.add_menu_item(manager.opt_res_action, image)
        image = media.ImageManager.text("Back", font, color)
        menu.add_menu_item(manager.bac_action, image)
        return menu
    
    @staticmethod
    def get_opt_res_menu(manager):
        font = media.ImageManager.TTF_Title
        color = media.COL_Blue
        title = media.ImageManager.text("Resolution", font, color, 64)
        menu = MenuScreen(manager.screen, title)
        font = media.ImageManager.TTF_MenuItem
        color = media.COL_Red
        image = media.ImageManager.text("Low", font, color)
        menu.add_menu_item(manager.opt_res_low_action, image)
        image = media.ImageManager.text("Medium", font, color)
        menu.add_menu_item(manager.opt_res_med_action, image)
        image = media.ImageManager.text("High", font, color)
        menu.add_menu_item(manager.opt_res_hig_action, image)
        image = media.ImageManager.text("Back", font, color)
        menu.add_menu_item(manager.bac_action, image)
        return menu
    
    @staticmethod
    def get_sou_menu(manager):
        font = media.ImageManager.TTF_Title
        color = media.COL_Blue
        title = media.ImageManager.text("Sound", font, color, 64)
        menu = MenuScreen(manager.screen, title)
        font = media.ImageManager.TTF_MenuItem
        color = media.COL_Red
        image = media.ImageManager.text("On", font, color)
        menu.add_menu_item(manager.opt_sou_on_action, image)
        image = media.ImageManager.text("Off", font, color)
        menu.add_menu_item(manager.opt_sou_off_action, image)
        image = media.ImageManager.text("Back", font, color)
        menu.add_menu_item(manager.bac_action, image)
        return menu
        
    
    @staticmethod
    def get_abo_screen(manager):
        popup = MessagePopup(manager.screen, manager, manager.gui_stack.top())
        popup.add_text_line("PyDoodler")
        popup.add_text_line("Have fun doodling.")
        popup.add_text_line(" ")
        popup.add_text_line("Author: Juan Vercellone")
        popup.add_text_line("(juanjov@gmail.com)")
        popup.add_text_line(" ")
        popup.add_text_line("<Press Esc to go back>")
        return popup
