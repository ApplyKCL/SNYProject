from barcode import EAN8
from barcode.writer import ImageWriter


number = "90909090"
my_code = EAN8(number, writer=ImageWriter())
my_code.save("Barcode")





