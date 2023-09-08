from pyzbar.pyzbar import decode
from PIL import Image

def read_barcode(image):
    decoded_data = decode(Image.fromarray(image))
    
    if len(decoded_data) >= 1:
        return decoded_data[0].data.decode()