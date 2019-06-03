#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image


def main():
    base_img = Image.open('image/1.png')
    box = (166, 64, 320, 337)

    temp_img = Image.open('image/2.png')
    # temp_img = temp_img.crop((0,0,304,546))

    # temp_img = temp_img.rotate(180)
    temp_img = temp_img.resize((box[2] - box[0], box[3] - box[1]))

    base_img.paste(temp_img, box)

    base_img.save('out.png')


if __name__ == '__main__':
    main()
