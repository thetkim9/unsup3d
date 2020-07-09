FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-devel AS builder
ENV LANG C.UTF-8
RUN apt-get update
RUN conda install pytorch==1.2.0 torchvision==0.4.0 cudatoolkit=9.2 -c pytorch
RUN apt -y install python3-pip
RUN apt-get -y install curl gnupg locales unzip
RUN conda install -c menpo opencv
RUN conda install scikit-image matplotlib pyyaml
RUN pip3 install tensorboardX moviepy
RUN conda install torchvision
RUN export PATH=/usr/local/cuda/bin:$PATH
RUN export CPATH=/usr/local/cuda/include:$CPATH
RUN export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
RUN pip3 install facenet-pytorch
COPY . .
RUN apt -y install git
RUN conda install gxx_linux-64=7.3
RUN git clone https://github.com/daniilidis-group/neural_renderer.git
RUN cd neural_renderer && python setup.py install
RUN cd pretrained && sh download_pretrained_celeba.sh
EXPOSE 80
#CMD python3 -m demo.demo --input demo/images/human_face --result demo/results/human_face --checkpoint pretrained/pretrained_celeba/checkpoint030.pth

CMD python3 server.py