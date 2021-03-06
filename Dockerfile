FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-devel AS builder
ENV LANG C.UTF-8
RUN apt-get update
RUN conda install pytorch==1.2.0 torchvision==0.4.0 cudatoolkit=9.2 -c pytorch
RUN apt -y install python3-pip
#RUN pip3 install Flask-Limiter
#RUN pip3 install Pillow
#RUN pip3 install requests
RUN conda install -c anaconda flask
RUN conda install -c anaconda "Pillow<7"
RUN conda install -c anaconda requests
RUN apt-get -y install curl gnupg locales unzip
RUN conda install -c menpo opencv
RUN conda install scikit-image matplotlib pyyaml
#RUN pip3 install tensorboardX moviepy
RUN conda install -c conda-forge tensorboardx
RUN conda install -c conda-forge moviepy
#RUN conda install torchvision
RUN export PATH=/usr/local/cuda/bin:$PATH
RUN export CPATH=/usr/local/cuda/include:$CPATH
RUN export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
RUN conda install gxx_linux-64=7.3
RUN apt -y install git
RUN git clone https://github.com/daniilidis-group/neural_renderer.git
RUN cd neural_renderer && python setup.py install
RUN git clone https://github.com/timesler/facenet-pytorch.git facenet_pytorch
RUN apt-get -y install python3-flask
RUN curl -o pretrained_celeba.zip "https://www.robots.ox.ac.uk/~vgg/research/unsup3d/data/pretrained_celeba.zip" && unzip pretrained_celeba.zip
RUN mkdir pretrained
COPY pretrained pretrained
RUN mkdir pretrained/pretrained_celeba
RUN mv pretrained_celeba/checkpoint030.pth pretrained/pretrained_celeba
COPY . .
EXPOSE 80
CMD python3 server.py
#python3 -m demo.demo --gpu --render_video --detect_human_face --input demo/images/human_face --result demo/results/human_face --checkpoint pretrained/pretrained_celeba/checkpoint030.pth
