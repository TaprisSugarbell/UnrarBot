import random
from PIL import Image
from moviepy.editor import VideoFileClip


async def generate_screenshot(file, name: str = "./thumb.jpg"):
    clip = VideoFileClip(file)
    ss_img = int(clip.duration / random.randint(15, 30))
    frame = clip.get_frame(ss_img)
    nimage = Image.fromarray(frame)
    nimage.save(name)
    return name

