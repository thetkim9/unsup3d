from moviepy.editor import *

clip = (VideoFileClip("texture_animation.mp4"))
clip.write_gif("result.gif")