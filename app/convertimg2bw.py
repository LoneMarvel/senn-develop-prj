from PIL import Image

img = Image.open("./static/images/sennicon.png")
BaW = img.convert("L")
BaW.save("./static/images/senniconbw.png")
BaW.show()