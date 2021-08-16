import requests, os, time
from db_utils.db_declaration import PicDownload, PIC_DOWNLOAD_STATUS
from logger import logger

PIC_DIR = "pics/"
PIC_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/"
}

# 下载图片
def download_pic(url, name):
    req = requests.request("GET", url=url, headers = PIC_DEFAULT_HEADERS)
    if req.ok:
        if req.headers.get("content-length") == 0:
            return None
        with open(os.path.join(PIC_DIR, name), "wb") as p:
            p.write(req.content)
        logger.info("成功下载并保存图片 {}".format(url))
        return True
    else:
        logger.warning("下载图片失败 {}".format(url))
        return False

while True:
    pics = PicDownload.select().where(PicDownload.is_downloaded == PIC_DOWNLOAD_STATUS["waiting"]).limit(1)
    if len(pics) == 0:
        break
    else:
        pic = pics[0]
    if download_pic(pic.url, pic.file):
        pic.is_downloaded = PIC_DOWNLOAD_STATUS["downloaded"]
        pic.save()
    else:
        pic.is_downloaded = PIC_DOWNLOAD_STATUS["skipped"]
        pic.save()
        time.sleep(60)
    time.sleep(1)
logger.info("图片下载全部完成")