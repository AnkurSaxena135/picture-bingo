import glob
from os import path
from PIL import Image


RESIZED_W = 1200
RESIZED_H = 700


def get_paths_from_folder(folder: str) -> list[str]:
    paths = glob.glob(f"{folder}/*")
    return paths


def get_filename_from_path(paths: list[str]) -> list[str]:
    return [p.split("\\")[-1] for p in paths]


def load_images(paths: str) -> list[Image.Image]:
    return [Image.open(p) for p in paths]


def resize_images(images: list[Image.Image]) -> list[Image.Image]:
    return [im.resize((RESIZED_W, RESIZED_H), Image.ANTIALIAS) for im in images]


def save_images(images: list[Image.Image], folder: str, filenames: list[str]) -> None:
    for index, image in enumerate(images):
        save_path = path.join(folder, filenames[index])
        image.save(save_path)


def main():
    pwd = path.abspath(__file__)
    source = path.abspath(path.join(pwd, "..", "icons"))
    destination = path.abspath(path.join(pwd, "..", "resized"))

    image_paths = get_paths_from_folder(source)
    image_filenames = get_filename_from_path(image_paths)
    images = load_images(image_paths)
    resized_images = resize_images(images)
    save_images(resized_images, destination, image_filenames)


if __name__ == "__main__":
    main()
