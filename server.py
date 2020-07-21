from flask import Flask, render_template, request, send_file
#from flask_limiter import Limiter
from PIL import Image, ImageOps
#from subprocess import Popen, PIPE
#import shlex
from moviepy.editor import *
#import threading
import time
import shutil
import os
import sys
import io
from demo.utils import *

progressRates = {}
#subProcesses = {}
#terminated = {}

global model
model = None

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
    print(user_id, "hi1")
    human_face = Image.open(request.files['person_image'].stream)
    if(human_face.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 401

    print("hi2")
    path = os.path.join("demo/inputs", str(user_id))
    os.mkdir(path)
    dir1 = "demo/inputs/"+str(user_id)+"/"+str(user_id)+"."+human_face.format.lower()
    human_face.save(dir1)
    progressRates[user_id] = 10

    print("hi3")
    #new_stderr = io.StringIO()
    #sys.stderr.write("test1")
    #sys.stderr.write("test2")
    #output = new_stderr.getvalue()
    #print(output)
    #sys.stderr.write("test3")
    #output = new_stderr.getvalue()
    #print(output)

    print("hi4")
    input_dir = 'demo/inputs/' + str(user_id)
    result_dir = 'demo/outputs'
    im_list = [os.path.join(input_dir, f) for f in sorted(os.listdir(input_dir)) if is_image_file(f)]
    print("hi4.2")
    global model
    for im_path in im_list:
        # print("Processing {im_path}")
        pil_im = Image.open(im_path).convert('RGB')
        print("hi4.5")
        result_code = model.run(pil_im)
        progressRates[user_id] = 60
        if result_code == -1:
            #print("Failed! Skipping {im_path}")
            continue
        save_dir = os.path.join(result_dir, os.path.splitext(os.path.basename(im_path))[0])
        model.save_results(save_dir)
    progressRates[user_id] = 70

    '''
    if not terminated[user_id]:
      command_line = 'python3 -u -m demo.demo --input demo/inputs/'+str(user_id)+' --result demo/outputs '
      args = shlex.split(command_line)
      proc = Popen(args, stdout=PIPE, stderr=PIPE)
      global subProcesses
      subProcesses[user_id] = proc

      # 127 single characters stdout from subprocess
      #count = 0
      while proc.poll() is None:  # Check the the child process is still running
        data = proc.stderr.read(1)  # Note: it reads as binary, not text
        if data != str.encode(" ") and data != str.encode("") and data is not None:
          #print(user_id, progressRates[user_id], data, count)
          progressRates[user_id] += 0.6
          pass
    '''

    clip = (VideoFileClip("demo/outputs/"+str(user_id)+"/texture_animation.mp4"))
    clip.write_gif("demo/outputs/"+str(user_id)+"/outImg.gif")
    progressRates[user_id] = 90
    print("hi5")
    result = send_file("demo/outputs/"+str(user_id)+"/outImg.gif", mimetype='image/gif')
    return result

  except Exception:
    return {'error': 'cannot load your image files. check your image files'}, 403

@app.route('/setup/<int:user_id>')
def setup(user_id):
    global progressRates
    progressRates[user_id] = 0
    return "0"

@app.route('/progress/<int:user_id>')
def progress(user_id):
    global progressRates
    #output = new_stderr.getvalue()
    return str(progressRates[user_id])

@app.route('/remove/<int:user_id>')
def remove(user_id):
    path = os.path.join("demo/inputs", str(user_id))
    shutil.rmtree(path)
    path = os.path.join("demo/outputs", str(user_id))
    shutil.rmtree(path)
    progressRates[user_id] = 100
    return "0"

'''
@app.route('/stopsubp/<int:user_id>')
def stopsubp(user_id):
    global subProcesses
    terminated[user_id] = True
    if user_id in subProcesses.keys():
      subProcesses[user_id].terminate()
    return "0"
'''

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

@app.route('/healthz')
def health():
  return 200

if __name__ == '__main__':
    import argparse
    import demo.demo as demo
    parser = argparse.ArgumentParser(description='Demo configurations.')
    parser.add_argument('--input', default='demo/inputs', type=str,
                        help='Path to the directory containing input images')
    parser.add_argument('--result', default='demo/outputs', type=str,
                        help='Path to the directory for saving results')
    parser.add_argument('--checkpoint', default='./pretrained/pretrained_celeba/checkpoint030.pth', type=str,
                        help='Path to the checkpoint file')
    parser.add_argument('--output_size', default=128, type=int, help='Output image size')
    parser.add_argument('--gpu', default=True, action='store_true', help='Enable GPU')
    parser.add_argument('--detect_human_face', default=True, action='store_true',
                        help='Enable automatic human face detection. This does not detect cat faces.')
    parser.add_argument('--render_video', default=True, action='store_true', help='Render 3D animations to video')
    args = parser.parse_args()
    model = demo.Demo(args)

    app.run(debug=False, port=80, host='0.0.0.0', threaded=True)

