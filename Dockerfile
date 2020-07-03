FROM continuumio/anaconda3:latest
RUN apt-get update
RUN apt -y install python3-pip
RUN pip3 install scikit-image matplotlib pyyaml tensorboardX moviepy
RUN conda install pytorch torchvision==0.5.0 cudatoolkit -c pytorch
RUN apt-get -y install curl gnupg
RUN pip3 install neural_renderer_pytorch
RUN pip3 install facenet-pytorch
RUN pip3 install flask Flask-Limiter
RUN pip3 install Pillow
RUN pip3 install requests
RUN pip3 install torch

COPY . .
RUN cd pretrained && sh download_pretrained_celeba.sh
EXPOSE 80
CMD python3 -m demo.demo --input demo/images/human_face --result demo/results/human_face --checkpoint pretrained/pretrained_celeba/checkpoint030.pth
