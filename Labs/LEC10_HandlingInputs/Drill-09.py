"""DRILL #9: arrow-key movement with run and idle animations."""
from pathlib import Path
from math import hypot
from pico2d import *

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 600
FRAME_WIDTH, FRAME_HEIGHT = 100, 100
FRAME_COUNT = 8
ANIMATION_FPS = 10
MOVE_SPEED = 250
ARROW_KEYS = {SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN}
ASSET_DIR = Path(__file__).resolve().parent


class Boy:
    def __init__(self):
        self.x = CANVAS_WIDTH / 2
        self.y = CANVAS_HEIGHT / 2
        self.frame = 0.0
        self.pressed_keys = set()
        self.facing = 1  # 1: right, -1: left
        self.moving = False

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key in ARROW_KEYS:
            self.pressed_keys.add(event.key)
            if event.key == SDLK_LEFT:
                self.facing = -1
            elif event.key == SDLK_RIGHT:
                self.facing = 1
        elif event.type == SDL_KEYUP and event.key in ARROW_KEYS:
            self.pressed_keys.discard(event.key)
        elif event.type == SDL_WINDOWEVENT and event.event == SDL_WINDOWEVENT_FOCUS_LOST:
            self.pressed_keys.clear()

    def movement(self):
        dx = int(SDLK_RIGHT in self.pressed_keys) - int(SDLK_LEFT in self.pressed_keys)
        dy = int(SDLK_UP in self.pressed_keys) - int(SDLK_DOWN in self.pressed_keys)
        return dx, dy

    def update(self, dt):
        dx, dy = self.movement()
        length = hypot(dx, dy)
        moving = bool(length)
        if moving != self.moving:
            self.frame = 0.0
        self.moving = moving
        if dx:
            self.facing = 1 if dx > 0 else -1
        if moving:
            self.x += dx / length * MOVE_SPEED * dt
            self.y += dy / length * MOVE_SPEED * dt
        # Keep the complete 100x100 sprite inside the canvas, not just its center.
        self.x = max(FRAME_WIDTH / 2, min(self.x, CANVAS_WIDTH - FRAME_WIDTH / 2))
        self.y = max(FRAME_HEIGHT / 2, min(self.y, CANVAS_HEIGHT - FRAME_HEIGHT / 2))
        self.frame = (self.frame + ANIMATION_FPS * dt) % FRAME_COUNT

    def animation_row(self):
        # Sprite-sheet rows, measured from the bottom: left run, right run,
        # left idle, right idle. Vertical movement keeps the last facing.
        if self.moving:
            return 100 if self.facing == 1 else 0
        return 300 if self.facing == 1 else 200


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        grass = load_image(str(ASSET_DIR / 'grass.png'))
        character = load_image(str(ASSET_DIR / 'animation_sheet.png'))
        boy = Boy()
        running = True
        previous_time = get_time()
        while running:
            now = get_time()
            dt = min(now - previous_time, 0.05)
            previous_time = now
            for event in get_events():
                if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
                    running = False
                else:
                    boy.handle_event(event)
            if not running:
                break
            boy.update(dt)
            clear_canvas()
            grass.draw(CANVAS_WIDTH / 2, 30)
            character.clip_draw(int(boy.frame) * FRAME_WIDTH, boy.animation_row(),
                                FRAME_WIDTH, FRAME_HEIGHT, boy.x, boy.y)
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
