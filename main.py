import sys
import pygame
import gui



pygame.init()
m = gui.GuiManager()
m.main_menu()

event_handlers = {}
event_handlers[pygame.MOUSEBUTTONDOWN] = m.handle_event
event_handlers[pygame.MOUSEBUTTONUP] = m.handle_event
event_handlers[pygame.MOUSEMOTION] = m.handle_event
event_handlers[pygame.KEYDOWN] = m.handle_event
event_handlers[pygame.QUIT] = sys.exit

while 1:
    for e in pygame.event.get():
        try:
            event_handlers[e.type](e)
        except KeyError:
            continue

    m.show_current()
    pygame.display.update()
    pygame.display.flip()