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

        contenthappy = '還算高興'
        num = fa["smile"]
        if num > 0.9: contenthappy = '很開心'
        elif num > 0.5: contenthappy = '開心'
        elif num > 0.25: contenthappy = '有點開心'
        elif num < 0.05: contenthappy = '面無表情'

        contentbasic = '無法判讀'
        contenta = fa["gender"]
        num = fa["age"]
        if contenta == 'male':
            if num < 8: contentbasic = '男孩'
            elif num < 18: contentbasic = '少男'
            elif num < 32: contentbasic = '男青年'
            elif num < 46: contentbasic = '青壯男'
            elif num < 55: contentbasic = '中壯男'
            elif num < 66: contentbasic = '中年男性'
            elif num < 75: contentbasic = '初老男性'
            elif num < 85: contentbasic = '老當益壯'
            elif num > 84: contentbasic = '長壽男子'
        if contenta == 'female':
            if num < 8: contentbasic = '女孩'
            elif num < 16: contentbasic = '少女'
            elif num < 16: contentbasic = '碧玉年華'
            elif num < 32: contentbasic = '花樣年華'
            elif num < 46: contentbasic = '輕熟女'
            elif num < 55: contentbasic = '風韻猶存'
            elif num < 66: contentbasic = '中年女性'
            elif num < 75: contentbasic = '初老女性'
            elif num < 85: contentbasic = '邁入老年女性'
            elif num > 84: contentbasic = '長壽女子'

        contenta = fa_makeup["lipMakeup"]
        contentb = fa_makeup["eyeMakeup"]

        content1 = '素顏'
        if contenta == True:
            if contentb == True: content1 = '粉墨登場'
            else: content1 = '略施脂粉'

        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(
            origin, fr["width"], fr["height"], fill=False, linewidth=2, color='r')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1], "%s, %s, \n"%(contentbasic, contenthappy), fontproperties=font_prop,
                 fontsize=10, weight="bold", va="bottom", color='b')
        plt.text(origin[0], origin[1], "%s "%(content1), fontproperties=font_prop,
                 fontsize=10, weight="bold", va="bottom", color='red')
    _ = plt.axis("off")
    # plt.show()
    plt.savefig('{}_result{}'.format(os.path.splitext(image_url)[0], os.path.splitext(image_url)[1]))
