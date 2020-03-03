# -*- coding: utf-8 -*-
# author: seven

from PIL import Image
import pytesseract
import modules.request.req as req
import string
import itertools

ambiguityArr = [('1','7'),('3','8')]

def getVcode(img):
    vcode = _getVCodesOnce(img)
    if vcode and len(vcode) == 4:
        possibles = [_getAllPossiablity(item) for item in vcode]
        product = itertools.product(*tuple(possibles))
        vcodes = [''.join(list(item)) for item in product]
        return vcodes


def _getVCodesOnce(img):
    img = _transactImage(img)
    text = pytesseract.image_to_string(img,config='digits')
    textArr = [item for item in text if item in string.digits]
    return ''.join(textArr)

def _getAllPossiablity(item):
    for aset in ambiguityArr:
        if item in aset:
            return aset
    return tuple([item])

def _transactImage(img):
    img = img.convert("L")
    pixdata = img.load()
    w ,h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x,y] < 180:
                pixdata[x,y] = 0
            else:
                pixdata[x,y] = 255

    # 对二值化图片降噪
    pixdata = img.load()
    w,h = img.size
    # 8邻域算法
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:#上
                count = count + 1
            if pixdata[x,y+1] > 245:#下
                count = count + 1
            if pixdata[x-1,y] > 245:#左
                count = count + 1
            if pixdata[x+1,y] > 245:#右
                count = count + 1
            if pixdata[x-1,y-1] > 245:#左上
                count = count + 1
            if pixdata[x-1,y+1] > 245:#左下
                count = count + 1
            if pixdata[x+1,y-1] > 245:#右上
                count = count + 1
            if pixdata[x+1,y+1] > 245:#右下
                count = count + 1
            if count > 4:
                pixdata[x,y] = 255
    return img