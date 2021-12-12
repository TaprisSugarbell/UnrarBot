import os
import re
import glob
import random
import string
import rarfile
from .. import sayulogs
from rarfile import PasswordRequired


def random_key(_string=string.hexdigits, _range: int = 10):
    return "".join(random.choice(_string) for _ in range(_range))


def unrar_file(_path, _folder, pwd=None):
    prob = rarfile.is_rarfile(_path)
    if prob:
        try:
            etr = rarfile.RarFile(_path)
            etr.extractall(_folder)
        except PasswordRequired:
            # sayulogs.error("Error.", exc_info=e)
            etr = rarfile.RarFile(_path)
            etr.extractall(_folder, pwd=pwd)
    return _folder


def orderx(x: str):
    _all_ = x.split("/")
    xts = _all_[-1].split(".")
    stx = xts[0]
    # ext = xts[-1]
    return int([_ for _ in re.findall(r"\d*", stx) if _][0])


def iter_all(_path: str):
    if _path[-1] != "/":
        _path += "/"
    _get_paths = []
    _isdir = os.path.isdir(_path)
    if _isdir:
        _g = glob.glob(_path + "**", recursive=True)
        nw_lst = [_i.replace("\\", "/") for _i in _g]
        for i in nw_lst:
            if os.path.isdir(i):
                pass
            else:
                _get_paths.append(i)
    return _get_paths


async def file_recognize(filename, out="./"):
    file_type = "document"
    images = ["jpg", "png", "webp"]
    videos = ["mp4", "mkv", "webm"]
    songs = ["mp3", "FLAC", "m4a"]
    documents = ["zip", "rar", "apk"]
    direcs = {
        "photo": images,
        "video": videos,
        "audio": songs,
        "document": documents}
    try:
        ext = filename.split(".")[-1]
        for i in direcs:
            if ext in direcs[i]:
                file_type = i
                break
    except Exception as e:
        sayulogs.error("Error.", exc_info=e)
        file_type = None
        ext = None
    return {
        "file": filename,
        "type": file_type,
        "ext": ext}
