import glob
import os
import time
from random import randint
from PIL import Image


def getNewRandomIndex(max, currentIndices):
    if max < len(currentIndices):
        num = 0
    else:
        num = randint(0, max)

        while currentIndices.count(num):
            num = randint(0, max)

    return num


def generateCard(num_slots, maxIndex):

    currentCard = []

    for i in range(0, num_slots):
        currentCard.append(getNewRandomIndex(maxIndex, currentCard))

    return currentCard


def generateAllCardIndices(num_slots, num_images, num_cards):

    all_cards = []

    for i in range(0, num_cards):
        singleCard = generateCard(num_slots, num_images - 1)

        while all_cards.count(singleCard) >= 1:
            singleCard = generateCard(num_slots, num_images - 1)

        all_cards.append(singleCard)

    return all_cards


def generateCardImage(
    indices, imagePaths, nbRows, nbCols, skipMiddle, bgPaths, positions
):

    sources = []
    maxSize = [0, 0]

    for index in indices:
        src = Image.open(imagePaths[index])
        src = src.resize((1150, 1150), Image.NEAREST)
        sources.append(src)

        if src.size[0] > maxSize[0]:
            maxSize[0] = src.size[0]

        if src.size[1] > maxSize[1]:
            maxSize[1] = src.size[1]

    maxSize[0] += 10
    maxSize[1] += 10

    if len(bgPaths) > 0:
        image = Image.open(bgPaths[0])
    else:
        image = Image.new("RGB", (maxSize[0] * nbCols, maxSize[1] * nbRows))

    currentIndex = 0

    for col in range(0, nbCols):
        for row in range(0, nbRows):
            if skipMiddle and col == nbCols / 2 and row == nbRows / 2:
                if len(positions) == 0:
                    position = (
                        int(
                            maxSize[0] * col
                            + maxSize[0] / 2
                            - sources[currentIndex].size[0] / 2
                        ),
                        int(
                            maxSize[1] * row
                            + maxSize[1] / 2
                            - sources[currentIndex].size[1] / 2
                        ),
                    )
                else:
                    position = positions[currentIndex]
                image.paste(sources[currentIndex], position)
                currentIndex = currentIndex + 1

    return image


################################
# Script directory
def main():

    pwd = os.path.dirname(__file__)

    # list of image paths
    srcBackgrounds = pwd + "/images/background"
    srcImages = pwd + "/resized"
    outImages = pwd + "/result/" + time.strftime("%Y%m%d-%H%M%S") + "/"
    bgPaths = glob.glob(srcBackgrounds + "/*")
    imagePaths = glob.glob(srcImages + "/*")
    num_images = len(imagePaths)

    print(num_images, "images found")

    # number of images in each card
    num_slots = 16

    # number of cards
    num_cards = 80

    # number of rows
    nbRows = 4

    # number of columns
    nbCols = 4

    # Skip middle
    skipMiddle = False

    # Square positions in background
    squarePositions = []

    print("Generating {} cards with {} indices each".format(num_cards, num_slots))
    all_cards = generateAllCardIndices(num_slots, num_images, num_cards)

    if not os.path.exists(outImages):
        os.makedirs(outImages)

    cardNum = 0

    for indices in all_cards:
        result = generateCardImage(
            indices, imagePaths, nbRows, nbCols, skipMiddle, bgPaths, squarePositions
        )
        result.save(outImages + "card{}.jpg".format(cardNum))
        cardNum = cardNum + 1


if __name__ == "__main__":
    main()