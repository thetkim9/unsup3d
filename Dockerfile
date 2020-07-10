FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-devel AS builder
ENV LANG C.UTF-8
RUN apt-get update
RUN conda install pytorch==1.2.0 torchvision==0.4.0 cudatoolkit=9.2 -c pytorch
RUN apt -y install python3-pip
RUN pip3 install -U flask
RUN pip3 install Flask-Limiter
RUN pip3 install Pillow
RUN pip3 install requests
RUN apt-get -y install curl gnupg locales unzip
RUN conda install -c menpo opencv
RUN conda install scikit-image matplotlib pyyaml
RUN pip3 install tensorboardX moviepy
RUN conda install torchvision
RUN export PATH=/usr/local/cuda/bin:$PATH
RUN export CPATH=/usr/local/cuda/include:$CPATH
RUN export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
RUN pip3 install facenet_pytorch
COPY . .
RUN apt -y install git
RUN conda install gxx_linux-64=7.3
RUN git clone https://github.com/daniilidis-group/neural_renderer.git
RUN cd neural_renderer && python setup.py install
RUN cd pretrained && sh download_pretrained_celeba.sh
RUN git clone https://github.com/timesler/facenet-pytorch.git facenet_pytorch
RUN git clone https://github.com/pallets/flask.git flask
RUN git clone https://github.com/alisaifee/flask-limiter.git Flask-Limiter
RUN git clone https://github.com/python-pillow/Pillow.git Pillow
RUN git clone https://github.com/psf/requests.git requests
#RUN pip3 install -e git://github.com/hiidef/oauth2app.git#egg=flask
#RUN pip3 install -e git://github.com/hiidef/oauth2app.git#egg=flask-limiter
EXPOSE 80
CMD python3 server.py
#python3 -m demo.demo --gpu --render_video --detect_human_face --input demo/images/human_face --result demo/results/human_face --checkpoint pretrained/pretrained_celeba/checkpoint030.pth
