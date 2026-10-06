"""Automated regression tests for DRILL #9."""
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('Drill-09.py')
SPEC = importlib.util.spec_from_file_location('drill09', SCRIPT)
d = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(d)


def key(boy, event_type, value):
    boy.handle_event(SimpleNamespace(type=event_type, key=value))


class Drill09Tests(unittest.TestCase):
    def test_start_at_center_idle_right(self):
        b = d.Boy()
        self.assertEqual((b.x, b.y), (400, 300))
        self.assertEqual(b.animation_row(), 300)
        self.assertFalse(b.moving)

    def test_all_four_directions(self):
        cases = [(d.SDLK_LEFT, (375, 300)), (d.SDLK_RIGHT, (425, 300)),
                 (d.SDLK_UP, (400, 325)), (d.SDLK_DOWN, (400, 275))]
        for button, expected in cases:
            with self.subTest(button=button):
                b = d.Boy()
                key(b, d.SDL_KEYDOWN, button)
                b.update(0.1)
                self.assertEqual((b.x, b.y), expected)

    def test_held_key_and_release(self):
        b = d.Boy()
        key(b, d.SDL_KEYDOWN, d.SDLK_RIGHT)
        for _ in range(5):
            b.update(0.1)
        self.assertEqual(b.x, 525)
        key(b, d.SDL_KEYUP, d.SDLK_RIGHT)
        b.update(0.1)
        self.assertEqual(b.x, 525)
        self.assertFalse(b.moving)

    def test_left_right_run_and_idle_rows(self):
        for button, run_row, idle_row in [(d.SDLK_LEFT, 0, 200), (d.SDLK_RIGHT, 100, 300)]:
            with self.subTest(button=button):
                b = d.Boy()
                key(b, d.SDL_KEYDOWN, button)
                b.update(0.1)
                self.assertEqual(b.animation_row(), run_row)
                key(b, d.SDL_KEYUP, button)
                b.update(0.1)
                self.assertEqual(b.animation_row(), idle_row)

    def test_vertical_motion_retains_last_facing(self):
        b = d.Boy()
        key(b, d.SDL_KEYDOWN, d.SDLK_LEFT)
        b.update(0.1)
        key(b, d.SDL_KEYUP, d.SDLK_LEFT)
        key(b, d.SDL_KEYDOWN, d.SDLK_UP)
        b.update(0.1)
        self.assertEqual(b.animation_row(), 0)
        key(b, d.SDL_KEYUP, d.SDLK_UP)
        b.update(0.1)
        self.assertEqual(b.animation_row(), 200)

    def test_diagonal_speed_matches_axis_speed(self):
        b = d.Boy()
        key(b, d.SDL_KEYDOWN, d.SDLK_RIGHT)
        key(b, d.SDL_KEYDOWN, d.SDLK_UP)
        b.update(0.1)
        self.assertAlmostEqual(((b.x - 400) ** 2 + (b.y - 300) ** 2) ** 0.5, 25)

    def test_opposite_keys_cancel_and_release_restores(self):
        b = d.Boy()
        key(b, d.SDL_KEYDOWN, d.SDLK_LEFT)
        key(b, d.SDL_KEYDOWN, d.SDLK_RIGHT)
        b.update(0.1)
        self.assertEqual((b.x, b.y), (400, 300))
        self.assertFalse(b.moving)
        key(b, d.SDL_KEYUP, d.SDLK_RIGHT)
        b.update(0.1)
        self.assertEqual(b.x, 375)
        self.assertEqual(b.animation_row(), 0)

    def test_key_repeat_does_not_leave_stuck_movement(self):
        b = d.Boy()
        for _ in range(5):
            key(b, d.SDL_KEYDOWN, d.SDLK_RIGHT)
        key(b, d.SDL_KEYUP, d.SDLK_RIGHT)
        b.update(0.1)
        self.assertEqual(b.x, 400)

    def test_all_edges_and_corners_keep_full_sprite_visible(self):
        cases = [({d.SDLK_LEFT}, (50, 300)), ({d.SDLK_RIGHT}, (750, 300)),
                 ({d.SDLK_UP}, (400, 550)), ({d.SDLK_DOWN}, (400, 50)),
                 ({d.SDLK_LEFT, d.SDLK_DOWN}, (50, 50)),
                 ({d.SDLK_LEFT, d.SDLK_UP}, (50, 550)),
                 ({d.SDLK_RIGHT, d.SDLK_DOWN}, (750, 50)),
                 ({d.SDLK_RIGHT, d.SDLK_UP}, (750, 550))]
        for buttons, expected in cases:
            with self.subTest(buttons=buttons):
                b = d.Boy()
                b.pressed_keys.update(buttons)
                b.update(100)
                self.assertEqual((b.x, b.y), expected)
                for _ in range(10):
                    b.update(0.1)
                    self.assertEqual((b.x, b.y), expected)

    def test_idle_frames_animate_and_wrap(self):
        b = d.Boy()
        b.update(0.1)
        self.assertEqual(b.frame, 1)
        b.update(0.7)
        self.assertEqual(b.frame, 0)
        self.assertEqual(b.animation_row(), 300)

    def test_escape_and_window_close_exit_and_cleanup(self):
        for event in [SimpleNamespace(type=d.SDL_QUIT),
                      SimpleNamespace(type=d.SDL_KEYDOWN, key=d.SDLK_ESCAPE)]:
            with self.subTest(event=event), patch.object(d, 'open_canvas'), \
                    patch.object(d, 'load_image'), patch.object(d, 'get_time', return_value=0), \
                    patch.object(d, 'get_events', return_value=[event]), \
                    patch.object(d, 'close_canvas') as close:
                d.main()
                close.assert_called_once()

    def test_required_background_and_sprite_are_loaded_and_drawn(self):
        with patch.object(d, 'open_canvas'), patch.object(d, 'load_image') as load, \
                patch.object(d, 'get_time', return_value=0), \
                patch.object(d, 'get_events', side_effect=[[], [SimpleNamespace(type=d.SDL_QUIT)]]), \
                patch.object(d, 'clear_canvas'), patch.object(d, 'update_canvas'), \
                patch.object(d, 'delay'), patch.object(d, 'close_canvas'):
            d.main()
            self.assertEqual([c.args[0] for c in load.call_args_list],
                             [str(d.ASSET_DIR / 'TUK_GROUND.png'),
                              str(d.ASSET_DIR / 'animation_sheet.png')])
            load.return_value.draw.assert_called_once_with(400, 300, 800, 600)
            load.return_value.clip_draw.assert_called_once_with(0, 300, 100, 100, 400, 300)

    def test_assets_resolve_from_script_directory(self):
        self.assertTrue((d.ASSET_DIR / 'animation_sheet.png').is_file())
        self.assertTrue((d.ASSET_DIR / 'TUK_GROUND.png').is_file())
        self.assertEqual(d.ASSET_DIR, SCRIPT.resolve().parent)


if __name__ == '__main__':
    unittest.main()
