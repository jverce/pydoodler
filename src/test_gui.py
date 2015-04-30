import unittest
import pygame
import gui

class TestGuiScreen(unittest.TestCase):
    def setUp (self):
        pygame.init()
        self.m = gui.GuiManager()

    def test_screen_init(self):
        s = gui.Screen(self.m.screen)
        self.assertEqual(s.parent_screen, self.m.screen)
        self.assertEqual(s.screen, None)

    def test_screen_show(self):
        s = gui.Screen(self.m.screen)
        self.assertRaises(TypeError, s.show)

    def tearDown(self):
        pygame.quit()
        self.m = None

if __name__ == '__main__':
    unittest.main()
