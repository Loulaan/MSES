FROM pytorch/pytorch:latest

RUN apt-get update && apt-get install -y git && apt-get install wget -y && apt install -y libsm6 libxext6 && apt-get install libxrender-dev -y && apt-get install libglib2.0-0 -y
RUN cd .. && git clone https://github.com/Loulaan/MSES

WORKDIR /MSES

RUN rm Dockerfile && pip install cython && pip install filterpy && pip install -U -r requirements.txt

COPY /weights /MSES/weights
COPY /newData /MSES/newData

EXPOSE 8888
EXPOSE 6006

CMD ["/bin/bash"]