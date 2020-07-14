from flask import Flask, render_template, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps
from subprocess import Popen, PIPE
import shlex
from moviepy.editor import *
import os

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

  #print("hi0")
  if not request.files.get('person_image'):
    return {'error': 'must have a image of human face'}, 400

  try:
    #print("hi1")
    human_face = Image.open(request.files['person_image'].stream)
    if(human_face.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 401

    #print("hi2")
    dir1 = "demo/inputs/inImg."+human_face.format.lower()
    human_face.save(dir1)

    #print("hi3")
    command_line = 'python3 -m demo.demo --gpu --render_video --detect_human_face ' \
                   '--input demo/inputs --result demo/outputs ' \
                   '--checkpoint pretrained/pretrained_celeba/checkpoint030.pth'
    args = shlex.split(command_line)
    process = Popen(args, stdout=PIPE)
    while True:
      output = process.stdout.readline()
      if output == '' and process.poll() is not None:
        break
      if output:
        print output.strip()
    rc = process.poll()
    '''
    msg, err = proc.communicate()
    '''
    #print(msg)
    #print(err)

    #print("hi4.5")
    '''
    if msg!=None and len(msg)>0:
        return {'error': 'face not properly recognized. choose a photo with an upfront person.'}, 402
    '''

    #print("hi5")
    '''
    print(os.path.exists("demo/outputs/inImg/texture_animation.mp4"))
    for path, subdirs, files in os.walk("demo"):
      for name in files:
        print(os.path.join(path, name))
    for path, subdirs, files in os.walk("demo/outputs"):
      for name in files:
        print(os.path.join(path, name))
    '''
    clip = (VideoFileClip("demo/outputs/inImg/texture_animation.mp4"))
    #print("hi5.5")
    clip.write_gif("demo/outputs/outImg.gif")

    #print("hi6.0")
    result = send_file("demo/outputs/outImg.gif", mimetype='image/gif')

    return result

  except Exception:
    return {'error': 'cannot load your image files. check your image files'}, 403

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

if __name__ == '__main__':
  app.run(debug=False, port=80, host='0.0.0.0')

