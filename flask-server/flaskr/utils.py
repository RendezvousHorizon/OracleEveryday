import base64


def recognize(img):
    return '人'


def image2base64(image_path):
    with open(image_path, 'rb') as image_file:
        data = base64.b64encode(image_file.read())
        return data
