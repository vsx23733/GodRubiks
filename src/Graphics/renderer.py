import pygame
import sys
import os

def display():

    """Simple Start Screen Display"""

    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Rubik's Cube AI - Start Screen")
    screen.fill((245, 242, 226))
    pygame.display.flip()

    return screen

def start_screen():

    """Start Screen Functionality"""
    screen = display()
    background = pygame.Surface((1000, 600))
    image = pygame.Surface((290, 200))
    imagesPath = r"ezgif-split"


    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to Rubik's Cube AI", True, (0, 0, 0))

    text_rect = text.get_rect(center=(290, 50))
    screen.blit(text, text_rect)

    for i, imagePath in enumerate(os.listdir(imagesPath)):
        
        imageName = pygame.image.load(os.path.join(imagesPath, imagePath))
        screen.blit(background, (0, 0))
        image.blit(imageName, (0, 0))
        screen.blit(image, (175, 100))
        pygame.display.update()
        pygame.time.delay(10)
        
    pygame.display.flip()
    
    return screen

    
    



def main():

    '''
    Main Function
    '''

    pygame.init()
    screen = start_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                print("Key pressed. Starting...")
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()