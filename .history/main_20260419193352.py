import pygame, random, asyncio

class ParticlePrinciple:
    def __init__(self):
        self.particles = []

    def emit(self, screen):
        if self.particles:
            self.delete_particles()
            for p in self.particles:
                p[0][1] += p[2][0]
                p[0][0] += p[2][1]
                p[1] -= 0.2
                pygame.draw.circle(screen, pygame.Color('white'), p[0], int(p[1]))

    def add_particles(self):
        x, y = pygame.mouse.get_pos()
        r = 10
        dx = random.randint(-3, 3)
        dy = random.randint(-3, 3)
        self.particles.append([[x, y], r, [dx, dy]])

    def delete_particles(self):
        self.particles = [p for p in self.particles if p[1] > 0]


class ParticleNyan:
    def __init__(self):
        self.particles = []
        self.size = 12
        self.image1 = pygame.image.load('pic/theo1.png').convert_alpha()
        self.image2 = pygame.image.load('pic/theo2.png').convert_alpha()
        self.current_image = self.image1
        self.switch = False
        
    def emit(self, screen):
        if self.particles:
            self.delete_particles()
            for p in self.particles:
                p[0].x -= 1
                pygame.draw.rect(screen, p[1], p[0])

        self.draw(screen)

    def add_particles(self, offset, color):
        x, y = pygame.mouse.get_pos()
        y += offset
        rect = pygame.Rect(x - self.size//2, y - self.size//2, self.size, self.size)
        self.particles.append((rect, color))

    def delete_particles(self):
        self.particles = [p for p in self.particles if p[0].x > 0]

    def draw(self, screen):
        rect = self.current_image.get_rect(center=pygame.mouse.get_pos())
        screen.blit(self.current_image, rect)

    def switch_image(self):
        self.current_image = self.image1 if self.switch else self.image2
        self.switch = not self.switch


async def main():
    pygame.init()

    screen = pygame.display.set_mode((360, 640))
    clock = pygame.time.Clock()

   
    bg1 = pygame.transform.scale(pygame.image.load('pic/bg1.png'), (360, 640))
    bg2 = pygame.transform.scale(pygame.image.load('pic/bg2.png'), (360, 640))
    current_bg = bg1

    particle1 = ParticlePrinciple()
    particle2 = ParticleNyan()

 
    audio_ready = False

    PARTICLE_EVENT = pygame.USEREVENT + 1
    IMAGE_SWITCH_EVENT = pygame.USEREVENT + 2
    BG_SWITCH_EVENT = pygame.USEREVENT + 3

    pygame.time.set_timer(PARTICLE_EVENT, 40)
    pygame.time.set_timer(IMAGE_SWITCH_EVENT, 300)
    pygame.time.set_timer(BG_SWITCH_EVENT, 2000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
            if event.type == pygame.MOUSEBUTTONDOWN and not audio_ready:
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load('wave/Nyan_Cat1.ogg')
                    pygame.mixer.music.play(-1)
                    audio_ready = True
                except:
                    print("audio fail")

            if event.type == PARTICLE_EVENT:
                particle1.add_particles()
                particle2.add_particles(-30, pygame.Color("red"))
                particle2.add_particles(-18, pygame.Color("orange"))
                particle2.add_particles(-6, pygame.Color("yellow"))
                particle2.add_particles(6, pygame.Color("green"))
                particle2.add_particles(18, pygame.Color("blue"))
                particle2.add_particles(30, pygame.Color("purple"))

            if event.type == IMAGE_SWITCH_EVENT:
                particle2.switch_image()

            if event.type == BG_SWITCH_EVENT:
                current_bg = bg1 if current_bg == bg2 else bg2

       
        screen.fill((0,0,0))
        screen.blit(current_bg, (0, 0))

        particle1.emit(screen)
        particle2.emit(screen)

        pygame.display.update()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())