FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime
ENV LANG C.UTF-8
RUN apt-get update
RUN apt -y install python3-pip
RUN apt-get -y install curl gnupg locales unzip
RUN pip3 install scikit-image matplotlib pyyaml tensorboardX moviepy
RUN pip3 install torchvision==0.4.0
RUN export PATH=/usr/local/cuda/bin:$PATH
RUN export CPATH=/usr/local/cuda/include:$CPATH
RUN export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
RUN pip3 install facenet-pytorch \
    flask \
    Flask-Limiter \
    Pillow \
    requests
COPY . .
COPY --from=jonstonchan/opencv4:latest /etc/jonstonchan/jonstonchan.conf /jonstonchan.conf
RUN cd pretrained && sh download_pretrained_celeba.sh
EXPOSE 80
#CMD python3 -m demo.demo --input demo/images/human_face --result demo/results/human_face --checkpoint pretrained/pretrained_celeba/checkpoint030.pth
