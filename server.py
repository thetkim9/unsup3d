'''
import torch
model = torch.load("./pretrained/pretrained_celeba/checkpoint030.pth")
print(model)
'''
from flask import Flask, render_template, request, send_file
from flask_limiter import Limiter
from PIL import Image, ImageOps

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

  if not request.files.get('human_face'):
    return {'error': 'must have a image of human face'}, 400

  try:
    human_face = Image.open(request.files['human_face'].stream)
    if(human_face.format not in ['JPG', 'JPEG', 'PNG']):
      return {'error': 'image must be jpg, jpeg or png'}, 400

    dir1 = "images/person."+human_face.format.lower()
    human_face.save(dir1)
    #print("hi2")
    p = Popen(['./a.out'], shell=True, stdout=PIPE, stdin=PIPE)
    value = (dir1 + '\n').encode('UTF-8')  # Needed in Python 3.
    p.stdin.write(value)
    p.stdin.flush()
    value = (dir2 + '\n').encode('UTF-8')  # Needed in Python 3.
    p.stdin.write(value)
    p.stdin.flush()
    p.wait()
    #print("hi4")

    msg, err = p.communicate()

    if msg!=None and len(msg)>0:
        return {'error': 'face not properly recognized. choose a photo with an upfront person.'}, 400

    #print("hi5.5")
    result = send_file("./demo/results/human_face/001_face/texture_animation.mp4", mimetype='video/mp4')

    #print("hi6")
    return result

  except Exception:
    return {'error': 'can not load your image files. check your image files'}, 400

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

if __name__ == '__main__':
  app.run(debug=False, port=80, host='0.0.0.0')

