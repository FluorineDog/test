import sys
import sdl2
import sdl2.ext as sdlext

WHITE = sdlext.Color()
BLACK = sdlext.Color(0, 0, 0)


class SoftwareRenderer(sdlext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super().__init__(window)


    def render(self, sprites, x=None, y=None):
        sdlext.fill(self.surface, BLACK)
        super().render(sprites)



class Player(sdlext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


class Ball(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super().__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)
            sprite.x = min(self.maxx - swidth, sprite.x)
            sprite.y = min(self.maxx - sheight, sprite.y)


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx, self.vy = 0, 0




def run():
    WIDTH = 1600
    HEIGHT = 1200
    THICKNESS = 10
    LENGTH = 100
    RADIUS = 20
    sdlext.init()
    window = sdlext.Window("the PG", size=(WIDTH, HEIGHT))
    window.show()
    world = sdlext.World()

    spriterenderer = SoftwareRenderer(window)
    world.add_system(spriterenderer)
    factory = sdlext.SpriteFactory(sdlext.SOFTWARE)
    sp_paddle1 = factory.from_color(WHITE, (THICKNESS, LENGTH))
    sp_paddle2 = factory.from_color(WHITE, (THICKNESS, LENGTH))
    player1 = Player(world, sp_paddle1, 0, HEIGHT//2 - LENGTH//2)
    player2 = Player(world, sp_paddle2, WIDTH - THICKNESS, HEIGHT//2 - LENGTH//2)
    sp_ball = factory.from_color(WHITE, size=(RADIUS, RADIUS))
    movement = MovementSystem(0, 0, WIDTH, HEIGHT)
    world.add_system(movement)
    ball = Ball(world, sp_ball, WIDTH//2 - THICKNESS//2, HEIGHT//2 - RADIUS//2)
    ball.velocity.vx = 3

    running = True
    while running:
        events = sdlext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        world.process()
    return 0

if __name__ == "__main__":
    sys.exit(run())