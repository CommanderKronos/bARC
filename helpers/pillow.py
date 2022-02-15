from PIL import Image, ImageDraw, ImageFont


def bgsreportimg():
    img = Image.new('RGB', (200, 200))

    d1 = ImageDraw.Draw(img)

    d1.text((65, 10), "Sample Text", fill=(255, 0, 0))

    img.save('temp/bgsreport.png')


bgsreportimg()
