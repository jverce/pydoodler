import sys
import pygame


class EventHandler:
    def __init__(self):
        self.actions = {}
    
    def handle(self, event, arg):
        try:
            self.actions[event](arg)
        except KeyError:
            return


class MouseEvent:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos


class MenuMouseEventHandler(EventHandler):
    def __init__(self, menu):
        EventHandler.__init__(self)        
        self.menu = menu
        self.actions[pygame.MOUSEMOTION] = menu.select
        self.actions[pygame.MOUSEBUTTONDOWN] = menu.activate
        
    def handle(self, e):
        EventHandler.handle(self, e.type, e.pos)


class MenuScreenMouseEventHandler(EventHandler):
    def __init__(self, menu_screen):
        EventHandler.__init__(self)        
        self.menu_screen = menu_screen
        self.actions[pygame.MOUSEMOTION] = self.menu_screen.move
        
    def handle(self, e):
        EventHandler.handle(self, e.type, e.pos)


class DrawMouseEventHandler(EventHandler):
    def __init__(self, draw_screen):
        EventHandler.__init__(self)
        self.draw_screen = draw_screen
        self.actions[pygame.MOUSEMOTION] = self.draw_screen.move
        self.actions[pygame.MOUSEBUTTONUP] = self.draw_screen.out_canvas
        self.actions[pygame.MOUSEBUTTONDOWN] = self.draw_screen.in_canvas
    
    def handle(self, e):
        try:
            EventHandler.handle(self, e.type, e.pos)
        except AttributeError:
            return


class DrawKeyEventHandler(EventHandler):
    def __init__(self, draw_screen):
        EventHandler.__init__(self)
        self.draw_screen = draw_screen
        self.actions[pygame.K_SPACE] = self.draw_screen.clean
        self.actions[pygame.K_s] = self.draw_screen.save
        self.actions[pygame.K_ESCAPE] = self.draw_screen.pause
        self.actions[pygame.K_q] = sys.exit

    def handle(self, e):
        try:
            EventHandler.handle(self, e.key, None)
        except AttributeError:
            return


class PopupKeyEventHandler(EventHandler):
    def __init__(self, popup):
        EventHandler.__init__(self)
        self.popup = popup
        self.actions[pygame.K_ESCAPE] = self.popup.exit

    def handle(self, e):
        try:
            EventHandler.handle(self, e.key, None)
        except AttributeError:
            return


class PopupMouseEventHandler(EventHandler):
    def __init__(self, popup):
        EventHandler.__init__(self)
        self.popup = popup
        self.actions[pygame.MOUSEMOTION] = self.popup.move
    
    def handle(self, e):
        try:
            EventHandler.handle(self, e.type, e.pos)
        except AttributeError:
            return