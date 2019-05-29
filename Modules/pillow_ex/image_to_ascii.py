
import os
from PIL import Image


def get_ascii(r, g, b, alpha=256):
    ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = (r * 38 + g * 75 + b * 15) >> 7

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]


def main(filename):
    im = Image.open(filename)
    w = 100
    h = int(im.size[1]/(im.size[0]*2 / w))
    im = im.resize((w, h), Image.NEAREST)

    text = ''
    for i in range(h):
        for j in range(w):
            text += get_ascii(*im.getpixel((j, i)))
        text += '\n'
    print(text)
    with open('pic/xiaoyang.txt', 'w') as f:
        f.write(text)
    os.system('notepad pic/xiaoyang.txt')


if __name__ == '__main__':
    main('pic/xiaoyang.png')
