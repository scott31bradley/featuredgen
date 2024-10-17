from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import random
import os
from resizeimage import resizeimage
import time
import glob
import imageio

def get_resized_img(img_path, video_size):
    img = Image.open(img_path)
    width, height = video_size  # these are the MAX dimensions
    video_ratio = width / height
    img_ratio = img.size[0] / img.size[1]
    if video_ratio >= 1:  # the video is wide
        if img_ratio <= video_ratio:  # image is not wide enough
            width_new = int(height * img_ratio)
            size_new = width_new, height
        else:  # image is wider than video
            height_new = int(width / img_ratio)
            size_new = width, height_new
    else:  # the video is tall
        if img_ratio >= video_ratio:  # image is not tall enough
            height_new = int(width / img_ratio)
            size_new = width, height_new
        else:  # image is taller than video
            width_new = int(height * img_ratio)
            size_new = width_new, height
    return img.resize(size_new, resample=Image.LANCZOS)


def featuredgen(modelname):
    for count, f in enumerate(os.listdir("featured")):
        f_name, f_ext = os.path.splitext("featured/{}".format(f))
        f_name = str(count+1)

        new_name = f'featured/{f_name}{f_ext}'
        os.rename("featured/{}".format(f), new_name)

    modelname = modelname
    for i in range(1,4):
        get_resized_img('featured/{}.jpg'.format(i), [400,630]).save('featured/resized-{}.jpg'.format(i))
        img = Image.open('featured/resized-{}.jpg'.format(i))
        img = resizeimage.resize_cover(img, [400, 630])
        img.save('featured/e{}.jpg'.format(i), img.format)
        img.close()
        
    imgback = Image.new("RGB", (1200,630), color=000000)
    xs,y = imgback.size

    for i in range(1,4):
        img = Image.open('featured/e{}.jpg'.format(i))
        rgb_im = img.convert('RGB')
        rgb_im.save('featured/l{}.jpg'.format(i))

        pasteim = Image.open('featured/l{}.jpg'.format(i))
        w, h = pasteim.size

        if i == 1:
            offset = 0, 0
        elif i == 2:
            offset = 400,0
        else:
            offset = 800,0

        imgback.paste(Image.open('featured/l{}.jpg'.format(i)), offset)
        imgback.save('generated/{}.jpg'.format(modelname))

        