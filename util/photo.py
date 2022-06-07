from PIL import Image
import io


def save_photo(file, name, square=False):
    if square:
        img = Image.open(io.BytesIO(file)).convert('RGB')
        img_width, img_height = img.size
        crop = img_width if img_width <= img_height else img_height
        img.crop(((img_width - crop) // 2,
                  (img_height - crop) // 2,
                  (img_width + crop) // 2,
                  (img_height + crop) // 2)).save(name)
        return
    Image.open(io.BytesIO(file)).convert('RGB').save(name)
