import pygame
import pygame_widgets as pw
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from src.rubiksCube import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


class Button:
    def __init__(self, image_path, coords, surface, scale=(300, 300)):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect(topleft=coords)     
        self.surface = surface

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(pygame.mouse.get_pos())
        )



def display():

    """Simple Start Screen Display"""

    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Rubik's Cube AI")
    screen.fill((245, 242, 226))
    pygame.display.flip()

    return screen



def start_screen():
    """Start Screen Functionality"""
    screen = display()
    image = pygame.Surface((480, 360))
    imagesPath = r"C:\Users\axelo\Documents\Projects\Programming project\GodRubiks\ezgif-split"
    running = True
    clock = pygame.time.Clock()

    images = [pygame.image.load(os.path.join(imagesPath, imageName)).convert_alpha() for imageName in sorted(os.listdir(imagesPath))]
    frameIndex = 0

    # Welcome text display
    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to Rubik's Cube AI", True, (0, 0, 0))
    text_rect = text.get_rect(center=(675, 50))
    

    # Button display
    resolve_button = Button(r"C:\Users\axelo\Documents\Projects\Programming project\GodRubiks\img\resolveButton.png", coords=(250, 400), surface=screen)
    quit_button = Button(r"C:\Users\axelo\Documents\Projects\Programming project\GodRubiks\img\QuitButton.png", coords=(800, 400), surface=screen)

    

    while running:
        
        screen.blit(text, text_rect)
        resolve_button.draw()
        quit_button.draw()

        frame = images[frameIndex]
        screen.blit(frame, (400, 125))
        pygame.time.delay(30)
        frameIndex = (frameIndex + 1) % len(images) 
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                print("Key pressed. Starting...")
                running = False

            if resolve_button.is_clicked(event):
                screen = resolve_screen()

            if quit_button.is_clicked(event):
                running = False

    clock.tick(60)


    return screen

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (1280 / 720), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


def resolve_screen():

    pygame.init()

    screen = pygame.display.set_mode((1280, 720), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rubik's Cube AI")
    screen.fill((245, 242, 226))

    cube = RubikCube()

    running = True
    clock = pygame.time.Clock()
    
    init_gl()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #cube.render_3D()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main():

    '''
    Main Function
    '''

    pygame.init()
    screen = start_screen()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()