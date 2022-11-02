from PIL import Image
image22 = Image.open("./images/yay.png")
im1 = image22.resize((28,28))
im1.save('./images/WOW.png')

im2 = Image.open("./images/WOW.png",'r')


im3 = im2.convert('L')
im3.save('./images/test_gray.png')
print(list(im3.getdata()))