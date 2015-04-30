import pygame
import media



class MenuItem:
    def __init__(self, action, image, x, y):
        self.action = action
        self.image = image
        self.x = x
        self.y = y
        self.image_nsel = image
        self.image_sel = image.copy()
        sel_rect = pygame.Rect(0, image.get_rect().h - 1, image.get_rect().w, 2)
        pygame.draw.rect(self.image_sel, (255, 255, 0), sel_rect)
        
    def select(self):
        self.image = self.image_sel
        
    def unselect(self):
        self.image = self.image_nsel
        
    def get_rect(self):
        w = self.image.get_rect().w
        h = self.image.get_rect().h
        return pygame.Rect(self.x, self.y, w, h)
        
    def paint(self, canvas):
        canvas.blit(self.image, (self.x, self.y))
        
        
class Menu:
    def __init__(self, canvas):
        self.items = []
        self.height = 50
        self.x_offset = 10
        self.canvas = canvas
        self.selected_item = None
        self.select_actions = {}
        self.select_actions[True] = self.selected
        self.select_actions[False] = self.unselected
        
    def add(self, action, image):
        x = self.x_offset
        y = self.height * len(self.items)
        self.items.append(MenuItem(action, image, x, y))
        self.resize_canvas()
        
        
    def resize_canvas(self):
        items_widths = []
        for item in self.items:
            items_widths.append(item.get_rect().w + self.x_offset)
        new_w = max(items_widths) + self.x_offset
        new_h = len(self.items) * self.height
        self.canvas = pygame.transform.scale(self.canvas, (new_w, new_h))
        
    def select(self, mouse_pos):
        x, y = mouse_pos
        rect = pygame.Rect(x, y, 1, 1)
        self.selected_item = None        
        for item in self.items:
            is_selected = item.get_rect().colliderect(rect)
            self.select_actions[is_selected](item)
            
    def selected(self, item):
        self.selected_item = item        
        item.select()
        
    def unselected(self, item):
        item.unselect()
        
    def activate(self, arg):
        try:
            self.selected_item.action()
            media.AudioManager.play(media.AudioManager.SND_MenuItem)
        except AttributeError:
            return
        
    def paint(self, screen, x=0, y=0):
        self.canvas.fill((0, 0, 0))
        for i in range(0, len(self.items)):
            self.items[i].paint(self.canvas)
        screen.blit(self.canvas, (x, y))
        


