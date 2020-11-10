from os import path
import glob
import random
import pygame


SCREEN_TITLE = "Halloween Bingo"
SCREEN_W = 1150
SCREEN_H = 700
RGB_WHITE = (250, 250, 250)
IMAGE_ZERO_POS = (0, 0)


def get_paths_from_folder(folder) -> list:
    paths = glob.glob(f"{folder}/*")
    return paths


def load_images(image_paths) -> list:
    return [pygame.image.load(path) for path in image_paths]


def pause(clock):
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pause = False
            elif event.type == pygame.QUIT:
                pause = False
            else:
                clock.tick(0)


def main(images_folder):
    # Initialize screen
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption(SCREEN_TITLE)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(RGB_WHITE)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Load images
    images = load_images(get_paths_from_folder(images_folder))

    # Event loop
    play = True
    while play:
        clock.tick(20)
        image = random.choice(images)
        screen.blit(image, IMAGE_ZERO_POS)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    images.remove(image)
                    screen.blit(image, IMAGE_ZERO_POS)
                    pause(clock)
            if event.type == pygame.QUIT:
                play = False
        if len(images) == 0:
            play = False


if __name__ == "__main__":
    pwd = path.abspath(__file__)
    images_folder = path.abspath(path.join(pwd, "..", "resized"))
    main(images_folder)