import os
import sys
from ..helper import *
from .. import sayulogs
from shutil import rmtree
from pydub.utils import mediainfo
from pyrogram import Client, filters
from moviepy.editor import VideoFileClip
from ..helper.get_thumb import generate_screenshot
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio


async def get_input(_path, tmp_directory, mode=0):
    file_data = await file_recognize(_path)
    file_type = file_data["type"]
    if file_type == "video":
        thumbnail = await generate_screenshot(_path, tmp_directory + random_key() + ".jpg")
        clip = VideoFileClip(_path)
        size = clip.size
        height = size[1]
        width = size[0]
        duration = int(clip.duration)
        if thumbnail:
            return InputMediaVideo(_path,
                                   thumbnail,
                                   width=width,
                                   height=height,
                                   duration=duration)
        else:
            return InputMediaVideo(_path,
                                   width=width,
                                   height=height,
                                   duration=duration)
    elif file_type == "audio":
        duration = mediainfo(_path)["duration"]
        return InputMediaAudio(_path,
                               duration=duration)
    elif file_type == "photo" and mode == 0:
        return InputMediaPhoto(_path)
    else:
        return InputMediaDocument(_path)


@Client.on_message(filters.command(["unrar"]))
async def __unrar__(bot, update):
    print(update)
    chat_id = update.chat.id
    user_id = update.from_user.id
    pwd = update.text.split("/unrar")[-1].strip()
    tmp_directory = "./Downloads/" + str(user_id) + "/" + random_key() + "/"
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory, exist_ok=True)
    try:
        if hasattr(update, "reply_to_message"):
            reply_to_message = update.reply_to_message
            if hasattr(reply_to_message, "document"):
                document = reply_to_message.document
                if document.file_name.split(".")[-1] == "rar":
                    file_rar = await bot.download_media(document.file_id,
                                                        file_name=tmp_directory + document.file_name)
                    folder_un = unrar_file(file_rar, tmp_directory, pwd)
                    all_paths = iter_all(folder_un)
                    summ = 0
                    _iter = []
                    for path in all_paths:
                        file_data = await file_recognize(path)
                        file_type = file_data["type"]
                        if file_type == "video":
                            thumbnail = await generate_screenshot(path, tmp_directory + random_key() + ".jpg")
                            clip = VideoFileClip(path)
                            size = clip.size
                            height = size[1]
                            width = size[0]
                            duration = int(clip.duration)
                            if thumbnail:
                                _iter.append(InputMediaVideo(path,
                                                             thumbnail,
                                                             width=width,
                                                             height=height,
                                                             duration=duration))
                            else:
                                _iter.append(InputMediaVideo(path,
                                                             width=width,
                                                             height=height,
                                                             duration=duration))
                        elif file_type == "audio":
                            duration = mediainfo(path)["duration"]
                            _iter.append(InputMediaAudio(path,
                                                         duration=duration))
                        elif file_type == "photo":
                            await bot.send_document(chat_id,
                                                    document=path)
                            _iter.append(InputMediaPhoto(path))
                        else:
                            _iter.append(InputMediaDocument(path))
                        summ += 1
                        if len(_iter) == 10 or summ == len(all_paths):
                            await bot.send_media_group(chat_id,
                                                       media=_iter)
                            _iter.clear()
                    # if file_type == "video":
                    #     thumbnail = await generate_screenshot(path, tmp_directory+random_key()+".jpg")
                    #     clip = VideoFileClip(path)
                    #     size = clip.size
                    #     height = size[1]
                    #     width = size[0]
                    #     duration = int(clip.duration)
                    #     if thumbnail:
                    #         await bot.send_video(chat_id,
                    #                              width=width,
                    #                              height=height,
                    #                              video=path,
                    #                              duration=duration,
                    #                              thumb=thumbnail)
                    #     else:
                    #         await bot.send_video(chat_id,
                    #                              width=width,
                    #                              height=height,
                    #                              video=path,
                    #                              duration=duration)
                    # elif file_type == "audio":
                    #     await bot.send_audio(chat_id,
                    #                          audio=path)
                    # elif file_type == "photo":
                    #     await bot.send_photo(chat_id,
                    #                          photo=path)
                    # else:
                    #     await bot.send_document(chat_id,
                    #                             document=path)

    except Exception as e:
        sayulogs.error(e)
        e = sys.exc_info()
        err = '{}: {}'.format(str(e[0]).split("'")[1], e[1].args[0])
        # await bot.send_message(chat_id=1202071750, text=err)
        xxs = await bot.send_message(chat_id=chat_id, text=f"{err}\n📮 Envía este error a @SayuOgiwara")
        raise
    finally:
        rmtree(tmp_directory)

