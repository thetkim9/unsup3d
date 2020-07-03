FROM pytorch/pytorch:1.2-cuda10.0-cudnn7-devel

RUN apt-get update
RUN apt -y install python3-pip
RUN apt-get -y install curl gnupg
RUN pip3 install scikit-image matplotlib pyyaml tensorboardX moviepy
RUN pip3 install torchvision==0.5.0

RUN python3 -c "import os; print(os.environ.get('CUDA_PATH'))"
RUN python3 -c "import torch; torch.cuda.is_available()"

RUN pip3 install neural_renderer_pytorch \
    facenet-pytorch \
    flask \
    Flask-Limiter \
    Pillow \
    requests

COPY . .
RUN cd pretrained && sh download_pretrained_celeba.sh
EXPOSE 80
CMD python3 -m demo.demo --input demo/images/human_face --result demo/results/human_face --checkpoint pretrained/pretrained_celeba/checkpoint030.pth
