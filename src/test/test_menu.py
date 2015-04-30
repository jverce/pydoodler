import sys
sys.path.append('..')

import unittest
import pygame
import menu

class TestMenuItem(unittest.TestCase):
    def setUp (self):
        pygame.init()
        self.w, self.h = 8, 8
        self.x, self.y = 0, 0
        self.s = pygame.Surface((self.w, self.h))
        self.m = menu.Menu(self.s)
        self.mi = menu.MenuItem(self.bogus_func, self.s, self.x, self.y)

    def bogus_func(self):
        return self

    def test_init(self):
        self.assertIsNotNone(self.mi.action)
        self.assertIsNotNone(self.mi.image)
        self.assertIsNotNone(self.mi.image_nsel)
        self.assertIsNotNone(self.mi.image_sel)
        self.assertEqual(self.mi.x, self.x)
        self.assertEqual(self.mi.y, self.y)

    def test_select(self):
        self.mi.select()
        self.assertEqual(self.mi.image, self.mi.image_sel)

    def test_unselect(self):
        self.mi.unselect()
        self.assertEqual(self.mi.image, self.mi.image_nsel)

    def test_get_rect(self):
        r = self.mi.get_rect()
        self.assertIsNotNone(r)
        self.assertEqual(r.w, self.w)
        self.assertEqual(r.h, self.h)

    def tearDown(self):
        pygame.quit()


class TestMenu(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.w, self.h = 8, 8
        self.x, self.y = 0, 0
        self.s = pygame.Surface((self.w, self.h))
        self.m = menu.Menu(self.s)
    
    def bogus_func(self):
        return self

    def test_init(self):
        self.assertIsNotNone(self.m.items)
        self.assertEqual(len(self.m.items), 0)
        self.assertEqual(self.m.height, 50)
        self.assertEqual(self.m.x_offset, 10)
        self.assertEqual(self.m.canvas, self.s)
        self.assertIsNone(self.m.selected_item)
        self.assertIsNotNone(self.m.select_actions)
        self.assertEqual(len(self.m.select_actions.keys()), 2)

    def test_add(self):
        n_items = len(self.m.items)
        self.m.add(self.bogus_func, self.s)
        self.assertEqual(len(self.m.items), n_items+1)
        self.assertEqual(self.m.items[-1].x, self.m.x_offset)
        self.assertEqual(self.m.items[-1].y, self.m.height*n_items)

    def test_resize_canvas(self):
        old_rect = self.m.canvas.get_rect()
        self.m.add(self.bogus_func, self.s)
        self.m.resize_canvas()
        self.assertNotEqual(self.m.canvas.get_rect, old_rect)

    def test_select(self):
        self.m.select((self.x, self.y))
        self.assertIsNone(self.m.selected_item)

    def test_selected(self):
        mi = menu.MenuItem(self.bogus_func, self.s, self.x, self.y)
        self.m.selected(mi)
        self.assertEqual(self.m.selected_item, mi)
        self.assertEqual(mi.image, mi.image_sel)

    def test_unselected(self):
        mi = menu.MenuItem(self.bogus_func, self.s, self.x, self.y)
        self.m.unselected(mi)
        self.assertEqual(mi.image, mi.image_nsel)

    # This function should not throw any exception
    def test_activate(self):
        self.m.activate(0)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()


