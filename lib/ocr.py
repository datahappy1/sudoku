import itertools

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def ocr_core(filename, config):
    """
    This function will handle the core OCR processing of images.
    """
    config = "'"+config+"'"
    text = pytesseract.image_to_string(Image.open(filename), config=config)
    return text


psm = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
oem = [0, 1, 2, 3]

cc = list(itertools.product(psm, oem))
for c in cc:
    com = '--psm '+str(c[0])+' --oem '+str(c[1])+'--l eng -c tessedit_char_whitelist=|_-0123456789'
    print(com)
    print(ocr_core('test.PNG', com))
