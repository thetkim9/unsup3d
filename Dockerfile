FROM jonstonchan/opencv4:latest
COPY . .
RUN apt-get update
RUN apt -y install python3-pip
RUN pip3 install flask 
RUN pip3 install Flask-Limiter
RUN pip3 install Pillow
RUN pip3 install requests
RUN apt-get -y install curl gnupg locales unzip
EXPOSE 80
#CMD python3 -m demo.demo --input demo/images/human_face --result demo/results/human_face --checkpoint pretrained/pretrained_celeba/checkpoint030.pth
CMD python3 server.py
