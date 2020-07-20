from flask import Flask, render_template, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps
from subprocess import Popen, PIPE
import shlex
from moviepy.editor import *
#import threading
#import time
import shutil
import os

progressRates = {}
subProcesses = {}
terminated = {}

app = Flask(__name__, static_url_path="", template_folder="./")
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 8

#limiter = Limiter(app, default_limits=['1 per second'])

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
    global progressRates
    user_id = int(request.form.get('user_id'))
    global terminated
    terminated[user_id] = False
    #print("hi1")
    human_face = Image.open(request.files['person_image'].stream)
    if(human_face.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 401

    #print("hi2")
    path = os.path.join("demo/inputs", str(user_id))
    os.mkdir(path)
    dir1 = "demo/inputs/"+str(user_id)+"/"+str(user_id)+"."+human_face.format.lower()
    human_face.save(dir1)
    progressRates[user_id] = 1

    if not terminated[user_id]:
      command_line = 'python3 -u -m demo.demo --input demo/inputs/'+str(user_id)+' --result demo/outputs '
      args = shlex.split(command_line)
      proc = Popen(args, stdout=PIPE, stderr=PIPE)
      global subProcesses
      subProcesses[user_id] = proc
      # 127 single characters stdout from subprocess
      count = 0
      while proc.poll() is None:  # Check the the child process is still running
        data = proc.stderr.read(1)  # Note: it reads as binary, not text
        if data != str.encode(" ") and data != str.encode("") and data is not None:
          #print(user_id, progressRates[user_id], data, count)
          progressRates[user_id] += 0.6
          pass

    clip = (VideoFileClip("demo/outputs/"+str(user_id)+"/texture_animation.mp4"))
    clip.write_gif("demo/outputs/"+str(user_id)+"/outImg.gif")

    #print("hi5")
    result = send_file("demo/outputs/"+str(user_id)+"/outImg.gif", mimetype='image/gif')
    return result

  except Exception:
    return {'error': 'cannot load your image files. check your image files'}, 403


@app.teardown_request
def show_teardown(exception):
    print(request.path, 'after with block', str(exception))


@app.route('/setup/<int:user_id>')
def setup(user_id):
    global progressRates
    progressRates[user_id] = 0
    return "0"

@app.route('/progress/<int:user_id>')
def progress(user_id):
    global progressRates
    return str(progressRates[user_id])

@app.route('/remove/<int:user_id>')
def remove(user_id):
    path = os.path.join("demo/inputs", str(user_id))
    shutil.rmtree(path)
    path = os.path.join("demo/outputs", str(user_id))
    shutil.rmtree(path)
    progressRates[user_id] = 100
    return "0"

@app.route('/stopsubp/<int:user_id>')
def stopsubp(user_id):
    global subProcesses
    terminated[user_id] = True
    if user_id in subProcesses.keys():
      subProcesses[user_id].terminate()
    return "0"

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

@app.route('/healthz')
def health():
  return 200

if __name__ == '__main__':
  app.run(debug=False, port=80, host='0.0.0.0')

