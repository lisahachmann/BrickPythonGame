import pygame

class MainApp():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((height,width))
        pygame.display.set_caption = ('Hello world!')

    def draw_background(self):
        WHITE = (255,255,255)
        self.screen.fill(WHITE)

    def draw_rectangles(self):
        rect_color = (255,0, 0)
        for i in range(5):
            rect = pygame.Rect((i*80,0),(80,30))
            line_width = 5
            pygame.draw.rect(self.screen, rect_color, rect, line_width)
    def draw_circle(self):
        circle_color = (0,0,255)
        circle_pos = (200, 350)
        pygame.draw.circle(self.screen, circle_color, circle_pos, 15)

    def main_loop(self):
        running = True
        while (running):
            self.draw_background()
            self.draw_rectangles()
            self.draw_circle()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    pass

if __name__ == "__main__":
    m = MainApp(400,400)
    m.main_loop()
