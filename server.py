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

'''
class ExportingThread(threading.Thread):
  def __init__(self):
    self.progress = 0
    super().__init__()

  def run(self):
    command_line = 'python3 -u -m demo.demo --gpu --render_video --detect_human_face ' \
                   '--input demo/inputs --result demo/outputs ' \
                   '--checkpoint pretrained/pretrained_celeba/checkpoint030.pth'
    args = shlex.split(command_line)

    proc = Popen(args, stdout=PIPE)
    # 131 single characters stdout from subprocess
    while proc.poll() is None:  # Check the the child process is still running
      data = proc.stdout.read(1)  # Note: it reads as binary, not text
      if data != str.encode(" ") and data != str.encode("") and data is not None:
        #print(data)
        self.progress += 0.76
'''

#exporting_threads = {}
progressRates = {}

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

  print("hi0")
  if not request.files.get('person_image'):
    return {'error': 'must have a image of human face'}, 400

  try:
    global progressRates
    user_id = int(request.form.get('user_id'))
    progressRates[user_id] = 0
    #print("hi1")
    human_face = Image.open(request.files['person_image'].stream)
    if(human_face.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 401

    #print("hi2")
    dir1 = "demo/inputs/"+str(user_id)+"."+human_face.format.lower()
    human_face.save(dir1)
    progressRates[user_id] = 5
    #global exporting_threads

    #thread_id = request.form['user_id']
    #exporting_threads[thread_id] = ExportingThread()
    #exporting_threads[thread_id].start()

    print("hi3")
    command_line = 'python3 -u -m demo.demo --gpu --render_video --detect_human_face ' \
                   '--input demo/inputs --result demo/outputs ' \
                   '--checkpoint pretrained/pretrained_celeba/checkpoint030.pth'
    args = shlex.split(command_line)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    # 127 single characters stdout from subprocess
    while proc.poll() is None:  # Check the the child process is still running
      data = proc.stderr.read(1)  # Note: it reads as binary, not text
      if data != str.encode(" ") and data != str.encode("") and data is not None:
        print(user_id, progressRates[user_id])
        progressRates[user_id] += 0.6
        pass
    #msg, err = p.communicate()
    #print(msg)
    #print(err)

    print("hi4")
    '''
    if msg!=None and len(msg)>0:
        return {'error': 'face not properly recognized. choose a photo with an upfront person.'}, 402
    '''
    '''
    print(os.path.exists("demo/outputs/inImg/texture_animation.mp4"))
    for path, subdirs, files in os.walk("demo"):
      for name in files:
        print(os.path.join(path, name))
    for path, subdirs, files in os.walk("demo/outputs"):
      for name in files:
        print(os.path.join(path, name))
    '''
    clip = (VideoFileClip("demo/outputs/"+str(user_id)+"/texture_animation.mp4"))
    clip.write_gif("demo/outputs/"+str(user_id)+"/outImg.gif")

    print("hi5")
    result = send_file("demo/outputs/"+str(user_id)+"/outImg.gif", mimetype='image/gif')
    path = os.path.join("demo/outputs", str(user_id))
    shutil.rmtree(path)
    progressRates[user_id] = 100
    return result

  except Exception:
    return {'error': 'cannot load your image files. check your image files'}, 403

'''
@app.route('/progress/<int:user_id>')
def progress(user_id):
    global exporting_threads

    return str(exporting_threads[user_id].progress)
'''
@app.route('/progress/<int:user_id>')
def progress(user_id):
    global progressRates
    if user_id not in progressRates.keys():
      #print("start")
      progressRates[user_id] = 0
    #print(progressRates[user_id])
    return str(progressRates[user_id])

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

if __name__ == '__main__':
  app.run(debug=False, port=80, host='0.0.0.0')

