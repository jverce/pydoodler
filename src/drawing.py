import time
import pygame
import media



class ColorPanel:
    def __init__(self, pos=(0, 0)):
        self.x, self.y = pos
        self.border_padding = 10
        self.border_col = (0, 127, 127)
        self.items = []
        self.positions = []
        self.current_col = media.COL_Black
        self.current_col_box_h = 50
        self.num_rows = 0
        self.select_actions = {}
        self.select_actions[True] = self.selected
    
    def add_color_item(self, item):        
        self.num_rows += 1
        vertical_pos = self.num_rows - 1
        rect_h = item.get_rect().h
        x = self.border_padding
        y = vertical_pos * rect_h + self.border_padding
        self.items.append(item)
        self.positions.append((x, y))
        
    def get_back_size(self):
        total_w = 0
        total_h = 0
        for i in self.items:
            total_w += i.get_rect().w
            total_h += i.get_rect().h
        total_w /= self.num_rows
        total_h /= len(self.items)
        total_h *= self.num_rows
        total_w += 2 * self.border_padding
        total_h += 2 * self.border_padding
        return (total_w, total_h)
    
    def get_size(self):
        b_w, b_h = self.get_back_size()
        b_h += self.current_col_box_h
        return (b_w, b_h)
    
    def get_rect(self):
        w, h = self.get_size()
        return pygame.Rect(self.x, self.y, w, h)
        
    def draw_background(self, screen):
        total_w, total_h = self.get_back_size()        
        rect = pygame.Rect(self.x, self.y, total_w, total_h)
        screen.fill(self.border_col, rect)
        rect = pygame.Rect(self.x, total_h, total_w, self.current_col_box_h)
        screen.fill(self.current_col, rect)
    
    def paint(self, screen):
        self.draw_background(screen)
        for i in range(0, len(self.items)):
            self.items[i].paint(screen, self.positions[i])
        
    def select(self, pos):
        x, y = pos
        mouse_rect = pygame.Rect(x, y, 1, 1)
        for pos in self.positions:
            index = self.positions.index(pos)
            item = self.items[index]
            item_size = item.get_rect().size
            rect = pygame.Rect(pos[0], pos[1], item_size[0], item_size[1])
            mouse_in = mouse_rect.colliderect(rect)
            try:
                self.select_actions[mouse_in](item.color)
            except KeyError:
                continue
    
    def selected(self, color):
        self.current_col = color


class ColorItem:
    def __init__(self, color, dim=(50, 25)):
        w, h = dim
        self.color = color
        self.rect = pygame.Surface((w, h))
    
    def get_rect(self):
        return self.rect.get_rect()
    
    def paint(self, screen, pos=(0, 0)):
        x, y = pos
        self.rect.fill(self.color) 
        screen.blit(self.rect, (x, y))
        

class DrawCanvas:
    def __init__(self, dim, color_panel):
        self.w, self.h = dim
        self.color_panel = color_panel
        self.back_color = media.COL_White
        self.canvas = pygame.Surface((self.w, self.h))
        self.canvas.fill(self.back_color)
        self.last_point = None
    
    def add_point(self, pos):
        x, y = pos
        color = self.color_panel.current_col
        try:
            pygame.draw.line(self.canvas, color, self.last_point, (x, y), 6)
        except TypeError:
            dot = pygame.Rect(x, y, 6, 6)
            self.canvas.fill(color, dot)
        self.last_point = (x, y)
    
    def release_mouse(self):
        self.last_point = None
    
    def paint(self, screen):
        screen.blit(self.canvas, (0, 0))
    
    def clean(self):
        self.canvas.fill(self.back_color)
    
    def save(self, area):
        image = self.canvas.subsurface(area)
        t = time.localtime()
        filename = str(t.tm_year) + "_"
        filename += str(t.tm_mon) + "_"
        filename += str(t.tm_mday) + "_"
        filename += str(t.tm_hour) + "_"
        filename += str(t.tm_min) + ".png"
        pygame.image.save(image, filename)
