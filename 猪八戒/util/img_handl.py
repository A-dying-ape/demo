# coding:utf-8
import os
import sys
import subprocess


def showImage(img_path):
    try:
        if sys.platform.find('darwin') >= 0: subprocess.call(['open', img_path])
        elif sys.platform.find('linux') >= 0: subprocess.call(['xdg-open', img_path])
        else: os.startfile(img_path)
    except:
        from PIL import Image
        img = Image.open(img_path)
        img.show()
        img.close()


def removeImage(img_path):
    if sys.platform.find('darwin') >= 0:
        os.system("osascript -e 'quit app \"Preview\"'")
    os.remove(img_path)


def saveImage(img, img_path):
    if os.path.isfile(img_path):
        os.remove(img_path)
    fp = open(img_path, 'wb')
    fp.write(img)
    fp.close()