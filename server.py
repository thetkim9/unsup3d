from flask import Flask, render_template, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps
from subprocess import Popen, PIPE
import shlex
from moviepy.editor import *

app = Flask(__name__,template_folder="./")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 8

limiter = Limiter(app, default_limits=['1 per second'])

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/render3D', methods=['GET', 'POST'])
def render3D():
  if request.method != "POST":
    return

  print("hi0")
  if not request.files.get('person_image'):
    return {'error': 'must have a image of human face'}, 400

  try:
    print("hi1")
    human_face = Image.open(request.files['person_image'].stream)
    if(human_face.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 400

    print("hi2")
    dir1 = "demo/inputs/inImg."+human_face.format.lower()
    human_face.save(dir1)

    print("hi3")
    command_line = 'python3.6 -m demo.demo --gpu --render_video --detect_human_face ' \
                   '--input demo/inputs --result demo/outputs ' \
                   '--checkpoint pretrained/pretrained_celeba/checkpoint030.pth'
    args = shlex.split(command_line)
    p = Popen(args,
              shell=True, stdout=PIPE, stdin=PIPE)
    print("hi3.5")
    value = (dir1 + '\n').encode('UTF-8')  # Needed in Python 3.
    p.stdin.write(value)
    p.stdin.flush()
    p.wait()
    print("hi4")

    msg, err = p.communicate()

    print("hi4.5")
    if msg!=None and len(msg)>0:
        return {'error': 'face not properly recognized. choose a photo with an upfront person.'}, 400

    print("hi5")
    clip = (VideoFileClip("demo/outputs/texture_animation.mp4"))
    clip.write_gif("outImg.gif")

    print("hi5.5")
    result = send_file("demo/outputs/outImg.gif", mimetype='image/gif')

    #print("hi6")
    return result

  except Exception:
    return {'error': 'cannot load your image files. check your image files'}, 400

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

if __name__ == '__main__':
  app.run(debug=False, port=80, host='0.0.0.0')

