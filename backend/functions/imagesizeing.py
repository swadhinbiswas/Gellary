from PIL import Image

class Getpicture:
  def crop(image:str, x:int, y:int, width:int, height:int):
    img = Image.open(image)
    img = img.crop((x, y, x+width, y+height))
    img.save(image)
    return image
  def resize(image:str, width:int, height:int):
    img = Image.open(image)
    img = img.resize((width, height))
    img.save(image)
    return image
  def rotate(image:str, degree:int):
    img = Image.open(image)
    img = img.rotate(degree)
    img.save(image)
    return image
  def flip(image:str, direction:str):
    img = Image.open(image)
    if direction == "horizontal":
      img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
      img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(image)
    return image
  def convert(image:str, format:str):
    img = Image.open(image)
    img.save(image, format)
    return image
  def getinfo(image:str):
    img = Image.open(image)
    return img.info
  def getformat(image:str):
    img = Image.open(image)
    return img.format
  def getmode(image:str):
    img = Image.open(image)
    return img.mode
  def getsize(image:str):
    img = Image.open(image)
    return img.size
  def getdata(image:str):
    img = Image.open(image)
    return img.getdata()
  def getcolors(image:str):
    img = Image.open(image)
    return img.getcolors()
  def getextrema(image:str):
    img = Image.open(image)
    return img.getextrema()
  def getbbox(image:str):
    img = Image.open(image)
    return img.getbbox()
  def getbands(image:str):
    img = Image.open(image)
    return img.getbands()
  def getim(image:str):
    img = Image.open(image)
    return img.getim()
  def getpalette(image:str):
    img = Image.open(image)
    return img.getpalette()
  def getpixel(image:str, x:int, y:int):
    img = Image.open(image)
    return img.getpixel((x, y))
  def getprojection(image:str):
    img = Image.open(image)
    return img.getprojection()
  def getcolors(image:str):
    img = Image.open(image)
    return img.getcolors()