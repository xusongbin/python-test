#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image


def main():
    base_img = Image.open('image/1.png')
    temp_img = Image.open('image/2.png')
    save_img = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    box = (166, 64, 320, 337)

    temp_img = temp_img.convert('RGBA')
    temp_img = temp_img.resize((box[2] - box[0], box[3] - box[1]))

    save_img.paste(temp_img, box)
    save_img.paste(base_img, (0, 0), base_img)

    save_img.save('mask.png')


if __name__ == '__main__':
    main()
