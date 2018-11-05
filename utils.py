import os
import requests
import matplotlib.pyplot as plt

from PIL import Image
from io import BytesIO
from matplotlib import patches
from matplotlib.font_manager import FontProperties

font_prop = FontProperties(fname=r"./fonts/NotoSansCJK-Black.ttc", size=14)


def export_ms_result_images(image_url, faces):
    """
    Export "Microsoft Face API: Python SDK" response into image
    """
    image = Image.open(image_url)
    plt.figure(figsize=(8, 8))
    ax = plt.imshow(image, alpha=0.6)
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        fa_makeup = face["faceAttributes"]["makeup"]

        content = '有些開心'
        num = fa["smile"]
        if num > 0.7:
            content = '開心'
        elif num < 0.1:
            content = '不開心'

        contenta = fa_makeup["eyeMakeup"]
        content1 = '沒有化妝'
        if contenta:
            content1 = '有化妝'

        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(
            origin, fr["width"], fr["height"], fill=False, linewidth=2, color='r')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1], "%s, %d, \n"%(fa["gender"].capitalize(), fa["age"]), 
                fontsize=16, weight="bold", va="bottom", color='b')
        plt.text(origin[0], origin[1], "%s, %s, %s, %s, \n"%("開心指數", fa["smile"],"(滿分為1)", content), fontproperties=font_prop,
                fontsize=9, weight="bold", va="bottom", color='red')
        plt.text(origin[0], origin[1], "%s, %s"%("有沒有化妝?", content1), fontproperties=font_prop,
                fontsize=8, weight="bold", va="bottom", color='purple')
    _ = plt.axis("off")
    # plt.show()
    plt.savefig('{}_result{}'.format(os.path.splitext(image_url)[0], os.path.splitext(image_url)[1]))
