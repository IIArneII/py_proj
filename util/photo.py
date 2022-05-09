from PIL import Image
import io


def save_photo(file, name):
    Image.open(io.BytesIO(file)).convert('RGB').save(name)
